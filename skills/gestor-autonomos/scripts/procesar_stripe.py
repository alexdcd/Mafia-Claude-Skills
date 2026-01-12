#!/usr/bin/env python3
"""
Procesador de Ingresos de Stripe/Substack para Autónomos en España.

Soporta CSVs de:
- Stripe Dashboard (exportación estándar)
- Substack (exportación de suscriptores/pagos)

REGLAS FISCALES APLICADAS:
1. El precio cobrado INCLUYE el IVA (Tax Inclusive)
   - Para clientes UE: Base = Total / 1.21, IVA = Total - Base
   - Para clientes no-UE: Base = Total, IVA = 0 (exportación exenta)

2. La territorialidad se determina por PAÍS del cliente, NO por moneda
   - Prioridad: country (billing) > country (ip)
   - Un pago en EUR desde Chile → exportación exenta (sin IVA)

3. Los fees (Substack + Stripe) son gastos deducibles para IRPF
"""

import argparse
import csv
import json
import sys
import re
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date
from typing import List, Dict, Tuple, Optional
import urllib.request

# Países UE-27 (sin UK desde 2021)
PAISES_UE = {
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
    'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL',
    'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'
}

NOMBRES_PAISES = {
    'AT': 'Austria', 'BE': 'Bélgica', 'BG': 'Bulgaria', 'HR': 'Croacia',
    'CY': 'Chipre', 'CZ': 'Rep. Checa', 'DK': 'Dinamarca', 'EE': 'Estonia',
    'FI': 'Finlandia', 'FR': 'Francia', 'DE': 'Alemania', 'GR': 'Grecia',
    'HU': 'Hungría', 'IE': 'Irlanda', 'IT': 'Italia', 'LV': 'Letonia',
    'LT': 'Lituania', 'LU': 'Luxemburgo', 'MT': 'Malta', 'NL': 'Países Bajos',
    'PL': 'Polonia', 'PT': 'Portugal', 'RO': 'Rumanía', 'SK': 'Eslovaquia',
    'SI': 'Eslovenia', 'ES': 'España', 'SE': 'Suecia',
    'US': 'EEUU', 'CA': 'Canadá', 'CL': 'Chile', 'PE': 'Perú',
    'MX': 'México', 'AR': 'Argentina', 'CO': 'Colombia', 'GB': 'Reino Unido',
}

# Tipos de cambio por defecto
TIPOS_CAMBIO = {
    'EUR': Decimal('1.0'),
    'USD': Decimal('0.92'),
    'GBP': Decimal('1.17'),
    'CAD': Decimal('0.68'),
    'CHF': Decimal('1.05'),
    'MXN': Decimal('0.054'),
    'CLP': Decimal('0.00092'),
    'PEN': Decimal('0.25'),
}

DIVISOR_IVA = Decimal('1.21')

def redondear(valor: Decimal) -> Decimal:
    """Redondea a 2 decimales."""
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def parsear_importe(valor: str) -> Tuple[Decimal, str]:
    """
    Parsea un importe con símbolo de moneda.
    Ejemplos: '€60.00', 'CA$140.00', '$50.00', '60.00'
    Returns: (importe, moneda)
    """
    if not valor or valor.strip() == '':
        return Decimal('0'), 'EUR'
    
    valor = str(valor).strip()
    
    # Detectar moneda por símbolo
    moneda = 'EUR'
    if valor.startswith('€'):
        moneda = 'EUR'
        valor = valor[1:]
    elif valor.startswith('CA$'):
        moneda = 'CAD'
        valor = valor[3:]
    elif valor.startswith('$'):
        moneda = 'USD'
        valor = valor[1:]
    elif valor.startswith('£'):
        moneda = 'GBP'
        valor = valor[1:]
    
    # Limpiar y convertir
    valor = valor.replace(',', '.').replace(' ', '').strip()
    try:
        return Decimal(valor), moneda
    except:
        return Decimal('0'), moneda

def parsear_fecha(valor: str) -> Optional[date]:
    """
    Parsea fechas en múltiples formatos.
    Substack: '02-Oct-25', '15-Nov-25'
    Stripe: '2025-10-02', '2025-10-02 14:30:00'
    """
    if not valor:
        return None
    
    valor = str(valor).strip()
    
    # Formato Substack: DD-MMM-YY
    try:
        return datetime.strptime(valor, '%d-%b-%y').date()
    except:
        pass
    
    # Formato ISO: YYYY-MM-DD
    try:
        return datetime.strptime(valor.split(' ')[0].split('T')[0], '%Y-%m-%d').date()
    except:
        pass
    
    # Formato europeo: DD/MM/YYYY
    try:
        return datetime.strptime(valor, '%d/%m/%Y').date()
    except:
        pass
    
    return None

def obtener_pais(pago: Dict) -> Optional[str]:
    """
    Obtiene el país del cliente.
    Prioridad: country (billing) > country (ip) > otros
    
    IMPORTANTE: Si hay country (billing), usarlo aunque esté vacío country (ip)
    """
    # Prioridad 1: country (billing)
    for campo in ['country (billing)', 'Country (billing)', 'billing_country']:
        pais = pago.get(campo, '').strip().upper()
        if pais and pais not in ['', 'NULL', 'NONE', 'N/A']:
            return pais
    
    # Prioridad 2: country (ip) - solo si no hay billing
    for campo in ['country (ip)', 'Country (ip)', 'ip_country']:
        pais = pago.get(campo, '').strip().upper()
        if pais and pais not in ['', 'NULL', 'NONE', 'N/A']:
            return pais
    
    # Otros campos
    for campo in ['Country', 'country', 'Card Country']:
        pais = pago.get(campo, '').strip().upper()
        if pais and pais not in ['', 'NULL', 'NONE', 'N/A']:
            return pais
    
    return None

def es_ue(pais: str) -> bool:
    """Verifica si un país está en la UE-27."""
    return pais.upper() in PAISES_UE if pais else False

def convertir_a_eur(importe: Decimal, moneda: str) -> Tuple[Decimal, Decimal]:
    """Convierte a EUR. Returns: (importe_eur, tipo_cambio)"""
    moneda = moneda.upper()
    if moneda == 'EUR':
        return importe, Decimal('1.0')
    tc = TIPOS_CAMBIO.get(moneda, Decimal('1.0'))
    return redondear(importe * tc), tc

def procesar_substack_stripe(
    pagos: List[Dict],
    trimestre: int,
    año: int
) -> Dict:
    """
    Procesa pagos de Substack o Stripe.
    """
    # Fechas del trimestre
    mes_inicio = (trimestre - 1) * 3 + 1
    mes_fin = trimestre * 3
    fecha_inicio = date(año, mes_inicio, 1)
    fecha_fin = date(año + 1, 1, 1) if mes_fin == 12 else date(año, mes_fin + 1, 1)
    
    # Acumuladores
    pagos_ue = []
    pagos_no_ue = []
    pagos_sin_pais = []
    
    total_bruto_ue = Decimal('0')
    total_base_ue = Decimal('0')
    total_iva_ue = Decimal('0')
    total_base_no_ue = Decimal('0')
    total_sin_pais = Decimal('0')
    
    total_substack_fee = Decimal('0')
    total_stripe_fee = Decimal('0')
    
    conversiones = {}
    paises_ue = {}
    paises_no_ue = {}
    
    for pago in pagos:
        try:
            # Parsear importe
            amount_raw = pago.get('amount', pago.get('Amount', '0'))
            importe, moneda_detectada = parsear_importe(amount_raw)
            
            if importe <= 0:
                continue
            
            # Moneda (puede venir en columna separada)
            moneda = pago.get('currency', pago.get('Currency', moneda_detectada)).upper()
            if moneda in ['EUR', 'CAD', 'USD', 'GBP']:
                pass
            else:
                moneda = moneda_detectada
            
            # Parsear fecha
            fecha_raw = pago.get('date', pago.get('Date', pago.get('created', pago.get('Created (UTC)', ''))))
            fecha = parsear_fecha(fecha_raw)
            
            # Filtrar por trimestre
            if fecha and not (fecha_inicio <= fecha < fecha_fin):
                continue
            
            # País (billing > ip)
            pais = obtener_pais(pago)
            
            # Convertir a EUR
            importe_eur, tc = convertir_a_eur(importe, moneda)
            
            # Registrar conversión
            if moneda != 'EUR':
                if moneda not in conversiones:
                    conversiones[moneda] = {'tc': str(tc), 'original': Decimal('0'), 'eur': Decimal('0'), 'count': 0}
                conversiones[moneda]['original'] += importe
                conversiones[moneda]['eur'] += importe_eur
                conversiones[moneda]['count'] += 1
            
            # Fees (Substack y Stripe)
            substack_fee_raw = pago.get('Substack fee', pago.get('substack_fee', '0'))
            stripe_fee_raw = pago.get('Stripe fee', pago.get('stripe_fee', '0'))
            
            substack_fee, _ = parsear_importe(substack_fee_raw)
            stripe_fee, _ = parsear_importe(stripe_fee_raw)
            
            # Convertir fees a EUR (misma moneda que el pago)
            substack_fee_eur, _ = convertir_a_eur(substack_fee, moneda)
            stripe_fee_eur, _ = convertir_a_eur(stripe_fee, moneda)
            
            total_substack_fee += substack_fee_eur
            total_stripe_fee += stripe_fee_eur
            
            # Calcular desglose IVA
            pais_es_ue = es_ue(pais) if pais else None
            
            # OPCIÓN CONSERVADORA: Sin país → tratar como UE (paga IVA)
            if pais_es_ue is True or pais_es_ue is None:
                # UE o sin país: IVA incluido → Base = Total / 1.21
                base = redondear(importe_eur / DIVISOR_IVA)
                iva = redondear(importe_eur - base)
                es_ue_final = True
            else:
                # No-UE: Exportación exenta
                base = importe_eur
                iva = Decimal('0')
                es_ue_final = False
            
            # Datos del pago
            pago_proc = {
                'fecha': str(fecha) if fecha else 'N/A',
                'email': pago.get('email', pago.get('Customer Email', ''))[:30],
                'importe_original': f"{importe:.2f} {moneda}",
                'total_eur': str(importe_eur),
                'base': str(base),
                'iva': str(iva),
                'pais': pais if pais else 'DESCONOCIDO',
                'substack_fee': str(substack_fee_eur),
                'stripe_fee': str(stripe_fee_eur),
            }
            
            # Clasificar
            if es_ue_final:
                # UE (incluye pagos sin país por criterio conservador)
                pagos_ue.append(pago_proc)
                total_bruto_ue += importe_eur
                total_base_ue += base
                total_iva_ue += iva
                pais_key = pais if pais else 'SIN_PAIS'
                paises_ue[pais_key] = paises_ue.get(pais_key, {'count': 0, 'total': Decimal('0')})
                paises_ue[pais_key]['count'] += 1
                paises_ue[pais_key]['total'] += importe_eur
                if not pais:
                    pagos_sin_pais.append(pago_proc)
                    total_sin_pais += importe_eur
            else:
                # No-UE (exportación)
                pagos_no_ue.append(pago_proc)
                total_base_no_ue += base
                paises_no_ue[pais] = paises_no_ue.get(pais, {'count': 0, 'total': Decimal('0')})
                paises_no_ue[pais]['count'] += 1
                paises_no_ue[pais]['total'] += importe_eur
                
        except Exception as e:
            print(f"⚠️  Error: {e}", file=sys.stderr)
    
    # Formatear
    for m in conversiones:
        conversiones[m]['original'] = str(redondear(conversiones[m]['original']))
        conversiones[m]['eur'] = str(redondear(conversiones[m]['eur']))
    for p in paises_ue:
        paises_ue[p]['total'] = str(redondear(paises_ue[p]['total']))
    for p in paises_no_ue:
        paises_no_ue[p]['total'] = str(redondear(paises_no_ue[p]['total']))
    
    total_fees = total_substack_fee + total_stripe_fee
    total_ingresos = total_base_ue + total_base_no_ue
    rendimiento_neto = total_ingresos - total_fees
    total_bruto = total_bruto_ue + total_base_no_ue
    
    # Total pagos = UE + no-UE (sin_pais ya está incluido en UE)
    total_pagos = len(pagos_ue) + len(pagos_no_ue)
    
    return {
        'periodo': {
            'trimestre': trimestre,
            'año': año,
            'descripcion': f'{trimestre}T {año}'
        },
        'resumen': {
            'total_pagos': total_pagos,
            'total_bruto_eur': str(redondear(total_bruto)),
            'ue': {
                'cantidad': len(pagos_ue),
                'total_cobrado': str(redondear(total_bruto_ue)),
                'base_imponible': str(redondear(total_base_ue)),
                'iva_incluido': str(redondear(total_iva_ue)),
            },
            'no_ue': {
                'cantidad': len(pagos_no_ue),
                'base_imponible': str(redondear(total_base_no_ue)),
            },
            'sin_pais': {
                'cantidad': len(pagos_sin_pais),
                'total': str(redondear(total_sin_pais)),
            }
        },
        'fees': {
            'substack': str(redondear(total_substack_fee)),
            'stripe': str(redondear(total_stripe_fee)),
            'total': str(redondear(total_fees)),
        },
        'paises': {'ue': paises_ue, 'no_ue': paises_no_ue},
        'conversiones': conversiones,
        'modelo_303': {
            'casilla_01_base_21': str(redondear(total_base_ue)),
            'casilla_03_cuota_21': str(redondear(total_iva_ue)),
            'casilla_60_exportaciones': str(redondear(total_base_no_ue)),
        },
        'modelo_130': {
            'ingresos': str(redondear(total_ingresos)),
            'gastos_fees': str(redondear(total_fees)),
            'rendimiento_neto': str(redondear(rendimiento_neto)),
        },
        'detalle_ue': pagos_ue,
        'detalle_no_ue': pagos_no_ue,
        'detalle_sin_pais': pagos_sin_pais if pagos_sin_pais else None,
    }

def cargar_csv(archivo: str) -> List[Dict]:
    pagos = []
    with open(archivo, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pagos.append(row)
    return pagos

def cargar_json(archivo: str) -> List[Dict]:
    with open(archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data if isinstance(data, list) else data.get('data', [data])

def main():
    parser = argparse.ArgumentParser(
        description='Procesador de Ingresos Stripe/Substack para Autónomos',
        epilog="""
REGLAS APLICADAS:
  1. IVA INCLUIDO: Base = Total / 1.21 (para UE)
  2. Territorialidad por PAÍS (billing > ip), no por moneda
  3. Fees de Substack/Stripe = gastos deducibles IRPF

Ejemplo: python3 procesar_stripe.py --archivo pagos.csv --trimestre 4 --año 2025
        """
    )
    
    parser.add_argument('--archivo', required=True)
    parser.add_argument('--trimestre', type=int, required=True, choices=[1,2,3,4])
    parser.add_argument('--año', type=int, required=True)
    parser.add_argument('--formato', choices=['csv', 'json'], default='csv')
    parser.add_argument('--json', action='store_true', help='Salida JSON')
    parser.add_argument('--exportar', type=str)
    parser.add_argument('--offline', action='store_true')
    
    args = parser.parse_args()
    
    try:
        pagos = cargar_json(args.archivo) if args.formato == 'json' else cargar_csv(args.archivo)
        print(f"📥 {len(pagos)} registros cargados", file=sys.stderr)
        
        resultado = procesar_substack_stripe(pagos, args.trimestre, args.año)
        
        if args.exportar:
            with open(args.exportar, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
            print(f"✅ Exportado a {args.exportar}", file=sys.stderr)
        
        if args.json:
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        else:
            r = resultado['resumen']
            m303 = resultado['modelo_303']
            m130 = resultado['modelo_130']
            fees = resultado['fees']
            
            print("\n" + "="*70)
            print(f"   REPORTE FISCAL STRIPE/SUBSTACK - {resultado['periodo']['descripcion']}")
            print("="*70)
            
            print(f"\n📊 RESUMEN GENERAL")
            print(f"   Total pagos procesados:        {r['total_pagos']}")
            print(f"   Total cobrado (Bruto):     {float(r['total_bruto_eur']):>12,.2f} EUR")
            
            print(f"\n{'-'*70}")
            print(f"1. INGRESOS SUJETOS A IVA (CLIENTES UE)")
            print(f"{'-'*70}")
            print(f"   Pagos UE:                      {r['ue']['cantidad']}")
            print(f"   Total cobrado (Bruto):     {float(r['ue']['total_cobrado']):>12,.2f} EUR")
            print(f"\n   DESGLOSE (IVA incluido):")
            print(f"   Base Imponible:            {float(r['ue']['base_imponible']):>12,.2f} EUR")
            print(f"   IVA a repercutir (21%):    {float(r['ue']['iva_incluido']):>12,.2f} EUR")
            
            if resultado['paises']['ue']:
                print(f"\n   Por país:")
                for p, d in sorted(resultado['paises']['ue'].items(), key=lambda x: float(x[1]['total']), reverse=True):
                    if p == 'SIN_PAIS':
                        print(f"     ⚠️  SIN PAÍS (tratado como UE): {d['count']} pagos, {float(d['total']):,.2f} €")
                    else:
                        nombre = NOMBRES_PAISES.get(p, p)
                        print(f"     {p} ({nombre}): {d['count']} pagos, {float(d['total']):,.2f} €")
            
            print(f"\n{'-'*70}")
            print(f"2. INGRESOS EXENTOS DE IVA (EXPORTACIONES / NO-UE)")
            print(f"{'-'*70}")
            print(f"   Pagos no-UE:                   {r['no_ue']['cantidad']}")
            print(f"   Base Imponible (= Total):  {float(r['no_ue']['base_imponible']):>12,.2f} EUR")
            
            if resultado['paises']['no_ue']:
                print(f"\n   Por país:")
                for p, d in sorted(resultado['paises']['no_ue'].items(), key=lambda x: float(x[1]['total']), reverse=True):
                    nombre = NOMBRES_PAISES.get(p, p)
                    print(f"     {p} ({nombre}): {d['count']} pagos, {float(d['total']):,.2f} €")
            
            if resultado['conversiones']:
                print(f"\n{'-'*70}")
                print(f"💱 CONVERSIONES DE MONEDA")
                print(f"{'-'*70}")
                for m, d in resultado['conversiones'].items():
                    print(f"   {m}: {d['count']} pagos, TC={d['tc']}")
                    print(f"        {float(d['original']):,.2f} {m} → {float(d['eur']):,.2f} EUR")
            
            print(f"\n{'-'*70}")
            print(f"3. GASTOS DEDUCIBLES (COMISIONES / FEES)")
            print(f"{'-'*70}")
            print(f"   Substack Fees:             {float(fees['substack']):>12,.2f} EUR")
            print(f"   Stripe Fees:               {float(fees['stripe']):>12,.2f} EUR")
            print(f"   TOTAL GASTOS:              {float(fees['total']):>12,.2f} EUR")
            
            print(f"\n{'='*70}")
            print(f"📋 IMPORTES PARA DECLARACIONES")
            print(f"{'='*70}")
            
            print(f"""
   ┌────────────────────────────────────────────────────────────────┐
   │  MODELO 303 - IVA TRIMESTRAL                                   │
   ├────────────────────────────────────────────────────────────────┤
   │  Casilla 01 (Base imponible 21%):          {float(m303['casilla_01_base_21']):>12,.2f} EUR  │
   │  Casilla 03 (Cuota devengada 21%):         {float(m303['casilla_03_cuota_21']):>12,.2f} EUR  │
   │  Casilla 60 (Exportaciones exentas):       {float(m303['casilla_60_exportaciones']):>12,.2f} EUR  │
   └────────────────────────────────────────────────────────────────┘
""")
            print(f"""   ┌────────────────────────────────────────────────────────────────┐
   │  MODELO 130 - PAGO FRACCIONADO IRPF                            │
   ├────────────────────────────────────────────────────────────────┤
   │  Base imponible (UE + no-UE):             {float(m130['ingresos']):>12,.2f} EUR  │
   │  Gastos deducibles (fees):                 {float(m130['gastos_fees']):>12,.2f} EUR  │
   │  ────────────────────────────────────────────────────────────  │
   │  Rendimiento Neto:                         {float(m130['rendimiento_neto']):>12,.2f} EUR  │
   └────────────────────────────────────────────────────────────────┘
""")
            print(f"{'-'*70}")
            print(f"📌 METODOLOGÍA APLICADA")
            print(f"{'-'*70}")
            print(f"   • IVA INCLUIDO: Base = Total ÷ 1.21 para clientes UE")
            print(f"   • Territorialidad: Por PAÍS (billing > ip), no por moneda")
            print(f"   • Sin país identificado: Tratado como UE (criterio conservador)")
            print(f"   • Exportaciones: Clientes no-UE exentos de IVA")
            print(f"   • Fees: Gastos deducibles para IRPF (no para IVA)")
            print("="*70 + "\n")
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
