#!/usr/bin/env python3
"""
Procesador de Ingresos de Stripe para Autónomos en España.
- Extrae ingresos de un trimestre específico
- Convierte monedas a EUR
- Separa pagos UE (requieren IVA) vs no-UE (exentos)
- Genera resumen para declaraciones trimestrales

Uso con datos JSON de Stripe MCP o CSV exportado.
"""

import argparse
import json
import csv
import sys
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date
from typing import List, Dict, Tuple
import urllib.request
import urllib.error

# Países de la Unión Europea (2024-2025)
PAISES_UE = {
    'AT': 'Austria',
    'BE': 'Bélgica', 
    'BG': 'Bulgaria',
    'HR': 'Croacia',
    'CY': 'Chipre',
    'CZ': 'República Checa',
    'DK': 'Dinamarca',
    'EE': 'Estonia',
    'FI': 'Finlandia',
    'FR': 'Francia',
    'DE': 'Alemania',
    'GR': 'Grecia',
    'HU': 'Hungría',
    'IE': 'Irlanda',
    'IT': 'Italia',
    'LV': 'Letonia',
    'LT': 'Lituania',
    'LU': 'Luxemburgo',
    'MT': 'Malta',
    'NL': 'Países Bajos',
    'PL': 'Polonia',
    'PT': 'Portugal',
    'RO': 'Rumanía',
    'SK': 'Eslovaquia',
    'SI': 'Eslovenia',
    'ES': 'España',
    'SE': 'Suecia',
}

# Tipos de cambio por defecto (actualizables)
# Se intentará obtener tipos actuales de API
TIPOS_CAMBIO_DEFAULT = {
    'EUR': Decimal('1.0'),
    'USD': Decimal('0.92'),
    'GBP': Decimal('1.17'),
    'CHF': Decimal('1.05'),
    'JPY': Decimal('0.0061'),
    'CAD': Decimal('0.68'),
    'AUD': Decimal('0.60'),
    'MXN': Decimal('0.054'),
    'BRL': Decimal('0.16'),
    'PLN': Decimal('0.23'),
    'SEK': Decimal('0.087'),
    'DKK': Decimal('0.134'),
    'NOK': Decimal('0.084'),
    'CZK': Decimal('0.040'),
    'HUF': Decimal('0.0025'),
    'RON': Decimal('0.20'),
    'BGN': Decimal('0.51'),
    'HRK': Decimal('0.133'),
}

def redondear_centimos(valor: Decimal) -> Decimal:
    """Redondea a 2 decimales."""
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def obtener_tipos_cambio_online() -> Dict[str, Decimal]:
    """Intenta obtener tipos de cambio actuales del BCE."""
    try:
        # Usar API pública del BCE o alternativa
        url = "https://api.exchangerate-api.com/v4/latest/EUR"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            rates = {}
            for currency, rate in data.get('rates', {}).items():
                # Invertir porque necesitamos X -> EUR
                if rate > 0:
                    rates[currency] = redondear_centimos(Decimal('1') / Decimal(str(rate)))
            rates['EUR'] = Decimal('1.0')
            return rates
    except Exception as e:
        print(f"⚠️  No se pudieron obtener tipos de cambio online: {e}", file=sys.stderr)
        print("   Usando tipos de cambio por defecto.", file=sys.stderr)
        return TIPOS_CAMBIO_DEFAULT

def convertir_a_euros(
    importe: Decimal, 
    moneda: str, 
    tipos_cambio: Dict[str, Decimal]
) -> Tuple[Decimal, Decimal]:
    """
    Convierte un importe a euros.
    Returns: (importe_eur, tipo_cambio_usado)
    """
    moneda = moneda.upper()
    if moneda == 'EUR':
        return importe, Decimal('1.0')
    
    tipo = tipos_cambio.get(moneda)
    if tipo is None:
        raise ValueError(f"Moneda no soportada: {moneda}. Añádela a tipos_cambio.")
    
    importe_eur = redondear_centimos(importe * tipo)
    return importe_eur, tipo

def es_pais_ue(codigo_pais: str) -> bool:
    """Verifica si un país está en la UE."""
    return codigo_pais.upper() in PAISES_UE

def calcular_trimestre(fecha: date) -> Tuple[int, int]:
    """Retorna (trimestre, año) de una fecha."""
    trimestre = (fecha.month - 1) // 3 + 1
    return trimestre, fecha.year

def procesar_pagos_stripe(
    pagos: List[Dict],
    trimestre: int,
    año: int,
    tipos_cambio: Dict[str, Decimal] = None
) -> Dict:
    """
    Procesa una lista de pagos de Stripe.
    
    Args:
        pagos: Lista de objetos de pago (de MCP o CSV)
        trimestre: 1-4
        año: Año fiscal
        tipos_cambio: Diccionario de conversión de monedas
    
    Returns:
        Resumen con pagos UE, no-UE, totales y desglose
    """
    if tipos_cambio is None:
        tipos_cambio = obtener_tipos_cambio_online()
    
    # Calcular fechas del trimestre
    mes_inicio = (trimestre - 1) * 3 + 1
    mes_fin = trimestre * 3
    fecha_inicio = date(año, mes_inicio, 1)
    if mes_fin == 12:
        fecha_fin = date(año, 12, 31)
    else:
        fecha_fin = date(año, mes_fin + 1, 1)
    
    # Estructuras para resultados
    pagos_ue = []
    pagos_no_ue = []
    pagos_sin_pais = []
    
    total_ue_eur = Decimal('0')
    total_no_ue_eur = Decimal('0')
    total_sin_pais_eur = Decimal('0')
    
    conversiones_realizadas = {}
    
    for pago in pagos:
        # Extraer datos del pago (compatible con estructura Stripe)
        # Stripe devuelve amount en centavos
        try:
            # Detectar formato (MCP JSON vs CSV)
            if 'amount' in pago:
                # Formato Stripe API/MCP (centavos)
                importe_cents = int(pago.get('amount', 0))
                importe = Decimal(importe_cents) / Decimal('100')
            elif 'Amount' in pago:
                # Formato CSV exportado
                importe = Decimal(str(pago.get('Amount', '0')).replace(',', '.'))
            else:
                continue
            
            moneda = pago.get('currency', pago.get('Currency', 'EUR')).upper()
            
            # Fecha del pago
            fecha_raw = pago.get('created', pago.get('Created (UTC)', pago.get('Date', '')))
            if isinstance(fecha_raw, int):
                # Timestamp Unix
                fecha_pago = datetime.fromtimestamp(fecha_raw).date()
            elif isinstance(fecha_raw, str) and fecha_raw:
                # String de fecha
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']:
                    try:
                        fecha_pago = datetime.strptime(fecha_raw.split('T')[0].split(' ')[0], fmt.split(' ')[0]).date()
                        break
                    except:
                        continue
                else:
                    fecha_pago = None
            else:
                fecha_pago = None
            
            # Filtrar por trimestre
            if fecha_pago:
                if not (fecha_inicio <= fecha_pago < fecha_fin):
                    continue
            
            # Estado del pago (solo succeeded/paid)
            status = pago.get('status', pago.get('Status', 'succeeded')).lower()
            if status not in ['succeeded', 'paid', 'complete']:
                continue
            
            # País del cliente
            # Intentar múltiples campos donde puede estar el país
            pais = None
            
            # Desde billing_details
            billing = pago.get('billing_details', {})
            if isinstance(billing, dict):
                address = billing.get('address', {})
                if isinstance(address, dict):
                    pais = address.get('country')
            
            # Desde payment_method_details
            if not pais:
                pm_details = pago.get('payment_method_details', {})
                if isinstance(pm_details, dict):
                    card = pm_details.get('card', {})
                    if isinstance(card, dict):
                        pais = card.get('country')
            
            # Desde campos directos (CSV)
            if not pais:
                pais = pago.get('Card Country', pago.get('Country', pago.get('customer_country')))
            
            # Convertir a EUR
            importe_eur, tipo_cambio = convertir_a_euros(importe, moneda, tipos_cambio)
            
            # Registrar conversión si no es EUR
            if moneda != 'EUR':
                if moneda not in conversiones_realizadas:
                    conversiones_realizadas[moneda] = {
                        'tipo_cambio': str(tipo_cambio),
                        'total_original': Decimal('0'),
                        'total_eur': Decimal('0'),
                        'num_pagos': 0
                    }
                conversiones_realizadas[moneda]['total_original'] += importe
                conversiones_realizadas[moneda]['total_eur'] += importe_eur
                conversiones_realizadas[moneda]['num_pagos'] += 1
            
            # Datos del pago procesado
            pago_procesado = {
                'id': pago.get('id', pago.get('id (metadata)', '')),
                'fecha': str(fecha_pago) if fecha_pago else 'N/A',
                'importe_original': str(importe),
                'moneda': moneda,
                'importe_eur': str(importe_eur),
                'tipo_cambio': str(tipo_cambio),
                'pais': pais.upper() if pais else 'DESCONOCIDO',
                'email': pago.get('receipt_email', pago.get('Customer Email', '')),
                'descripcion': pago.get('description', pago.get('Description', ''))[:50]
            }
            
            # Clasificar por país
            if pais:
                pais = pais.upper()
                if es_pais_ue(pais):
                    pago_procesado['requiere_iva'] = True
                    pago_procesado['nombre_pais'] = PAISES_UE.get(pais, pais)
                    pagos_ue.append(pago_procesado)
                    total_ue_eur += importe_eur
                else:
                    pago_procesado['requiere_iva'] = False
                    pagos_no_ue.append(pago_procesado)
                    total_no_ue_eur += importe_eur
            else:
                pago_procesado['requiere_iva'] = None  # Indeterminado
                pagos_sin_pais.append(pago_procesado)
                total_sin_pais_eur += importe_eur
                
        except Exception as e:
            print(f"⚠️  Error procesando pago: {e}", file=sys.stderr)
            continue
    
    # Convertir Decimals a strings en conversiones
    for moneda in conversiones_realizadas:
        conversiones_realizadas[moneda]['total_original'] = str(
            redondear_centimos(conversiones_realizadas[moneda]['total_original'])
        )
        conversiones_realizadas[moneda]['total_eur'] = str(
            redondear_centimos(conversiones_realizadas[moneda]['total_eur'])
        )
    
    total_general = total_ue_eur + total_no_ue_eur + total_sin_pais_eur
    
    # IVA estimado para pagos UE (21% sobre base imponible)
    # Base = Total / 1.21 si ya incluye IVA, o Total si hay que añadirlo
    # En Substack, los precios NO incluyen IVA para clientes UE
    iva_ue_estimado = redondear_centimos(total_ue_eur * Decimal('0.21'))
    
    return {
        'periodo': {
            'trimestre': trimestre,
            'año': año,
            'descripcion': f'{trimestre}T {año}',
            'fecha_inicio': str(fecha_inicio),
            'fecha_fin': str(fecha_fin)
        },
        'resumen': {
            'total_pagos': len(pagos_ue) + len(pagos_no_ue) + len(pagos_sin_pais),
            'total_eur': str(redondear_centimos(total_general)),
            'pagos_ue': {
                'cantidad': len(pagos_ue),
                'total_eur': str(redondear_centimos(total_ue_eur)),
                'iva_a_declarar_21': str(iva_ue_estimado),
                'nota': 'Estos pagos requieren IVA. El IVA se calcula sobre la base (21%)'
            },
            'pagos_no_ue': {
                'cantidad': len(pagos_no_ue),
                'total_eur': str(redondear_centimos(total_no_ue_eur)),
                'nota': 'Pagos fuera de UE - Exentos de IVA (exportación de servicios)'
            },
            'pagos_sin_pais': {
                'cantidad': len(pagos_sin_pais),
                'total_eur': str(redondear_centimos(total_sin_pais_eur)),
                'nota': 'País desconocido - Revisar manualmente'
            }
        },
        'conversiones_moneda': conversiones_realizadas,
        'para_modelo_303': {
            'base_imponible_ue': str(redondear_centimos(total_ue_eur)),
            'iva_repercutido_ue': str(iva_ue_estimado),
            'exportaciones_no_ue': str(redondear_centimos(total_no_ue_eur)),
            'total_ingresos': str(redondear_centimos(total_general))
        },
        'para_modelo_130': {
            'ingresos_trimestre': str(redondear_centimos(total_general)),
            'nota': 'Total de ingresos sin IVA para cálculo de IRPF'
        },
        'detalle_ue': pagos_ue,
        'detalle_no_ue': pagos_no_ue,
        'detalle_sin_pais': pagos_sin_pais if pagos_sin_pais else None,
        'fecha_proceso': datetime.now().isoformat()
    }

def cargar_pagos_csv(archivo: str) -> List[Dict]:
    """Carga pagos desde un CSV exportado de Stripe."""
    pagos = []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pagos.append(row)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {archivo}")
    return pagos

def cargar_pagos_json(archivo: str) -> List[Dict]:
    """Carga pagos desde un JSON (output de Stripe MCP)."""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Puede ser una lista directa o tener estructura {data: [...]}
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'data' in data:
                return data['data']
            else:
                return [data]
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {archivo}")

def main():
    parser = argparse.ArgumentParser(
        description='Procesador de Ingresos de Stripe para Declaraciones Trimestrales',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Procesar CSV exportado de Stripe:
  python3 procesar_stripe.py --archivo pagos.csv --trimestre 4 --año 2024
  
  # Procesar JSON de Stripe MCP:
  python3 procesar_stripe.py --archivo charges.json --trimestre 1 --año 2025 --formato json
  
  # Procesar con tipos de cambio específicos:
  python3 procesar_stripe.py --archivo pagos.csv --trimestre 4 --año 2024 --tipo-cambio USD:0.93 GBP:1.18

Formatos CSV soportados:
  - Exportación estándar de Stripe Dashboard
  - Columnas esperadas: Amount, Currency, Created (UTC), Card Country, Status
        """
    )
    
    parser.add_argument('--archivo', type=str, required=True, help='Archivo CSV o JSON con pagos')
    parser.add_argument('--trimestre', type=int, required=True, choices=[1, 2, 3, 4], help='Trimestre (1-4)')
    parser.add_argument('--año', type=int, required=True, help='Año fiscal')
    parser.add_argument('--formato', choices=['csv', 'json'], default='csv', help='Formato del archivo (default: csv)')
    parser.add_argument('--tipo-cambio', nargs='*', help='Tipos de cambio personalizados (ej: USD:0.93 GBP:1.18)')
    parser.add_argument('--offline', action='store_true', help='No intentar obtener tipos de cambio online')
    parser.add_argument('--json', action='store_true', help='Salida en formato JSON')
    parser.add_argument('--exportar', type=str, help='Exportar resultado a archivo JSON')
    
    args = parser.parse_args()
    
    try:
        # Cargar pagos
        if args.formato == 'json':
            pagos = cargar_pagos_json(args.archivo)
        else:
            pagos = cargar_pagos_csv(args.archivo)
        
        print(f"📥 Cargados {len(pagos)} registros de {args.archivo}", file=sys.stderr)
        
        # Obtener tipos de cambio
        if args.offline:
            tipos_cambio = TIPOS_CAMBIO_DEFAULT.copy()
        else:
            tipos_cambio = obtener_tipos_cambio_online()
        
        # Aplicar tipos de cambio personalizados
        if args.tipo_cambio:
            for tc in args.tipo_cambio:
                try:
                    moneda, valor = tc.split(':')
                    tipos_cambio[moneda.upper()] = Decimal(valor)
                except:
                    print(f"⚠️  Formato inválido: {tc}. Usar MONEDA:VALOR", file=sys.stderr)
        
        # Procesar
        resultado = procesar_pagos_stripe(pagos, args.trimestre, args.año, tipos_cambio)
        
        # Exportar si se solicita
        if args.exportar:
            with open(args.exportar, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
            print(f"✅ Resultado exportado a: {args.exportar}", file=sys.stderr)
        
        if args.json:
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        else:
            # Mostrar resumen en terminal
            print("\n" + "="*65)
            print(f"   INGRESOS STRIPE - {resultado['periodo']['descripcion']}")
            print("="*65)
            
            r = resultado['resumen']
            print(f"\n📊 RESUMEN GENERAL:")
            print(f"   Total pagos procesados:  {r['total_pagos']}")
            print(f"   Total en EUR:            {float(r['total_eur']):>12,.2f} €")
            
            print(f"\n🇪🇺 PAGOS UNIÓN EUROPEA (requieren IVA):")
            print(f"   Cantidad:                {r['pagos_ue']['cantidad']}")
            print(f"   Base imponible:          {float(r['pagos_ue']['total_eur']):>12,.2f} €")
            print(f"   IVA a declarar (21%):    {float(r['pagos_ue']['iva_a_declarar_21']):>12,.2f} €")
            
            print(f"\n🌍 PAGOS FUERA DE UE (exentos IVA):")
            print(f"   Cantidad:                {r['pagos_no_ue']['cantidad']}")
            print(f"   Total EUR:               {float(r['pagos_no_ue']['total_eur']):>12,.2f} €")
            
            if r['pagos_sin_pais']['cantidad'] > 0:
                print(f"\n⚠️  PAGOS SIN PAÍS (revisar):")
                print(f"   Cantidad:                {r['pagos_sin_pais']['cantidad']}")
                print(f"   Total EUR:               {float(r['pagos_sin_pais']['total_eur']):>12,.2f} €")
            
            # Conversiones de moneda
            if resultado['conversiones_moneda']:
                print(f"\n💱 CONVERSIONES DE MONEDA:")
                for moneda, conv in resultado['conversiones_moneda'].items():
                    print(f"   {moneda}: {conv['num_pagos']} pagos, "
                          f"{float(conv['total_original']):,.2f} {moneda} → "
                          f"{float(conv['total_eur']):,.2f} € (TC: {conv['tipo_cambio']})")
            
            print("\n" + "-"*65)
            print("📋 DATOS PARA DECLARACIONES:")
            m303 = resultado['para_modelo_303']
            print(f"\n   MODELO 303 (IVA):")
            print(f"   · Base imponible UE:     {float(m303['base_imponible_ue']):>12,.2f} €")
            print(f"   · IVA repercutido:       {float(m303['iva_repercutido_ue']):>12,.2f} €")
            print(f"   · Exportaciones no-UE:   {float(m303['exportaciones_no_ue']):>12,.2f} €")
            
            m130 = resultado['para_modelo_130']
            print(f"\n   MODELO 130 (IRPF):")
            print(f"   · Ingresos trimestre:    {float(m130['ingresos_trimestre']):>12,.2f} €")
            
            print("="*65 + "\n")
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
