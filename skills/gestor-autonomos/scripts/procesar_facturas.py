#!/usr/bin/env python3
"""
Procesador de Facturas para Autónomos en España.
Valida, calcula y genera resúmenes de facturas emitidas y recibidas.
"""

import argparse
import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import List, Dict, Optional
import re

# Tipos de IVA válidos en España
TIPOS_IVA = {
    'general': Decimal('21'),
    'reducido': Decimal('10'),
    'superreducido': Decimal('4'),
    'exento': Decimal('0')
}

# Retenciones IRPF comunes
TIPOS_RETENCION = {
    'profesional': Decimal('15'),
    'nuevo_autonomo': Decimal('7'),
    'arrendamiento': Decimal('19'),
    'sin_retencion': Decimal('0')
}

def redondear_centimos(valor: Decimal) -> Decimal:
    """Redondea a 2 decimales."""
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def validar_nif(nif: str) -> dict:
    """
    Valida un NIF/NIE/CIF español.
    Returns: dict con 'valido', 'tipo', y 'mensaje'
    """
    nif = nif.upper().replace(' ', '').replace('-', '')
    
    # NIF persona física (8 números + letra)
    if re.match(r'^[0-9]{8}[A-Z]$', nif):
        letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
        numero = int(nif[:8])
        letra_correcta = letras[numero % 23]
        if nif[8] == letra_correcta:
            return {'valido': True, 'tipo': 'NIF', 'mensaje': 'NIF válido'}
        else:
            return {'valido': False, 'tipo': 'NIF', 'mensaje': f'Letra incorrecta. Debería ser {letra_correcta}'}
    
    # NIE extranjero (X/Y/Z + 7 números + letra)
    if re.match(r'^[XYZ][0-9]{7}[A-Z]$', nif):
        letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
        primera = {'X': '0', 'Y': '1', 'Z': '2'}[nif[0]]
        numero = int(primera + nif[1:8])
        letra_correcta = letras[numero % 23]
        if nif[8] == letra_correcta:
            return {'valido': True, 'tipo': 'NIE', 'mensaje': 'NIE válido'}
        else:
            return {'valido': False, 'tipo': 'NIE', 'mensaje': f'Letra incorrecta. Debería ser {letra_correcta}'}
    
    # CIF empresa (letra + 8 caracteres)
    if re.match(r'^[ABCDEFGHJKLMNPQRSUVW][0-9]{7}[0-9A-J]$', nif):
        return {'valido': True, 'tipo': 'CIF', 'mensaje': 'CIF con formato válido'}
    
    return {'valido': False, 'tipo': 'DESCONOCIDO', 'mensaje': 'Formato no reconocido'}

def calcular_factura(
    base_imponible: Decimal,
    tipo_iva: Decimal = Decimal('21'),
    tipo_retencion: Decimal = Decimal('0')
) -> dict:
    """
    Calcula los importes de una factura.
    """
    cuota_iva = redondear_centimos(base_imponible * tipo_iva / Decimal('100'))
    retencion = redondear_centimos(base_imponible * tipo_retencion / Decimal('100'))
    total = redondear_centimos(base_imponible + cuota_iva - retencion)
    
    return {
        'base_imponible': str(base_imponible),
        'tipo_iva': str(tipo_iva),
        'cuota_iva': str(cuota_iva),
        'tipo_retencion': str(tipo_retencion),
        'retencion': str(retencion),
        'total': str(total)
    }

def procesar_csv(archivo: str, tipo: str) -> dict:
    """
    Procesa un archivo CSV de facturas.
    
    Formato CSV esperado:
    numero,fecha,nif,concepto,base_imponible,tipo_iva,tipo_retencion
    
    Args:
        archivo: Ruta al archivo CSV
        tipo: 'emitidas' o 'recibidas'
    
    Returns:
        Resumen con totales y lista de facturas procesadas
    """
    facturas = []
    errores = []
    
    total_base = Decimal('0')
    total_iva = Decimal('0')
    total_retencion = Decimal('0')
    total_facturas = Decimal('0')
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, start=2):  # Línea 2 en adelante (1 es cabecera)
                try:
                    base = Decimal(row.get('base_imponible', '0').replace(',', '.'))
                    iva = Decimal(row.get('tipo_iva', '21').replace(',', '.'))
                    ret = Decimal(row.get('tipo_retencion', '0').replace(',', '.'))
                    
                    calculo = calcular_factura(base, iva, ret)
                    
                    # Validar NIF
                    nif = row.get('nif', '')
                    validacion_nif = validar_nif(nif) if nif else {'valido': False, 'mensaje': 'NIF vacío'}
                    
                    factura = {
                        'linea': i,
                        'numero': row.get('numero', ''),
                        'fecha': row.get('fecha', ''),
                        'nif': nif,
                        'nif_valido': validacion_nif['valido'],
                        'concepto': row.get('concepto', ''),
                        **calculo
                    }
                    
                    if not validacion_nif['valido']:
                        factura['advertencia_nif'] = validacion_nif['mensaje']
                    
                    facturas.append(factura)
                    
                    # Acumular totales
                    total_base += Decimal(calculo['base_imponible'])
                    total_iva += Decimal(calculo['cuota_iva'])
                    total_retencion += Decimal(calculo['retencion'])
                    total_facturas += Decimal(calculo['total'])
                    
                except Exception as e:
                    errores.append({
                        'linea': i,
                        'error': str(e),
                        'datos': row
                    })
    
    except FileNotFoundError:
        return {'error': f'Archivo no encontrado: {archivo}'}
    except Exception as e:
        return {'error': f'Error leyendo archivo: {str(e)}'}
    
    return {
        'tipo': tipo,
        'archivo': archivo,
        'num_facturas': len(facturas),
        'num_errores': len(errores),
        'totales': {
            'base_imponible': str(redondear_centimos(total_base)),
            'iva': str(redondear_centimos(total_iva)),
            'retencion': str(redondear_centimos(total_retencion)),
            'total': str(redondear_centimos(total_facturas))
        },
        'facturas': facturas,
        'errores': errores if errores else None,
        'fecha_proceso': datetime.now().isoformat()
    }

def main():
    parser = argparse.ArgumentParser(
        description='Procesador de Facturas para Autónomos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Calcular una factura individual:
  python3 procesar_facturas.py --base 1000 --iva 21 --retencion 15
  
  # Procesar archivo CSV de facturas emitidas:
  python3 procesar_facturas.py --archivo facturas.csv --tipo emitidas
  
  # Validar un NIF:
  python3 procesar_facturas.py --validar-nif 12345678Z

Formato CSV esperado (con cabecera):
numero,fecha,nif,concepto,base_imponible,tipo_iva,tipo_retencion
F001,2024-01-15,B12345678,Servicios,1000,21,15
        """
    )
    
    # Modo cálculo individual
    parser.add_argument('--base', type=str, help='Base imponible para cálculo individual')
    parser.add_argument('--iva', type=str, default='21', help='Tipo de IVA (%)')
    parser.add_argument('--retencion', type=str, default='0', help='Tipo de retención IRPF (%)')
    
    # Modo proceso CSV
    parser.add_argument('--archivo', type=str, help='Archivo CSV a procesar')
    parser.add_argument('--tipo', choices=['emitidas', 'recibidas'], help='Tipo de facturas')
    
    # Validación NIF
    parser.add_argument('--validar-nif', type=str, help='Validar un NIF/NIE/CIF')
    
    # Formato salida
    parser.add_argument('--json', action='store_true', help='Salida en formato JSON')
    
    args = parser.parse_args()
    
    try:
        # Modo validación NIF
        if args.validar_nif:
            resultado = validar_nif(args.validar_nif)
            if args.json:
                print(json.dumps(resultado, indent=2, ensure_ascii=False))
            else:
                emoji = "✅" if resultado['valido'] else "❌"
                print(f"\n{emoji} {args.validar_nif}: {resultado['mensaje']} ({resultado['tipo']})\n")
            return
        
        # Modo cálculo individual
        if args.base:
            resultado = calcular_factura(
                Decimal(args.base),
                Decimal(args.iva),
                Decimal(args.retencion)
            )
            if args.json:
                print(json.dumps(resultado, indent=2, ensure_ascii=False))
            else:
                print("\n" + "="*45)
                print("   CÁLCULO DE FACTURA")
                print("="*45)
                print(f"   Base imponible:   {float(resultado['base_imponible']):>10,.2f} €")
                print(f"   IVA ({args.iva}%):        {float(resultado['cuota_iva']):>10,.2f} €")
                if float(resultado['retencion']) > 0:
                    print(f"   Retención ({args.retencion}%): -{float(resultado['retencion']):>10,.2f} €")
                print("-"*45)
                print(f"   TOTAL FACTURA:    {float(resultado['total']):>10,.2f} €")
                print("="*45 + "\n")
            return
        
        # Modo proceso CSV
        if args.archivo and args.tipo:
            resultado = procesar_csv(args.archivo, args.tipo)
            if args.json:
                print(json.dumps(resultado, indent=2, ensure_ascii=False))
            else:
                if 'error' in resultado:
                    print(f"\n❌ Error: {resultado['error']}\n")
                    return
                
                print("\n" + "="*55)
                print(f"   RESUMEN FACTURAS {args.tipo.upper()}")
                print("="*55)
                print(f"   Archivo:          {resultado['archivo']}")
                print(f"   Facturas:         {resultado['num_facturas']}")
                if resultado['num_errores'] > 0:
                    print(f"   ⚠️  Errores:       {resultado['num_errores']}")
                
                print(f"\n📊 TOTALES:")
                t = resultado['totales']
                print(f"   Base imponible:   {float(t['base_imponible']):>12,.2f} €")
                print(f"   IVA:              {float(t['iva']):>12,.2f} €")
                if float(t['retencion']) > 0:
                    print(f"   Retenciones:      {float(t['retencion']):>12,.2f} €")
                print("-"*55)
                print(f"   TOTAL:            {float(t['total']):>12,.2f} €")
                print("="*55 + "\n")
                
                # Mostrar advertencias de NIF
                nifs_invalidos = [f for f in resultado['facturas'] if not f.get('nif_valido', True)]
                if nifs_invalidos:
                    print("⚠️  NIFs con problemas:")
                    for f in nifs_invalidos:
                        print(f"   - Factura {f['numero']}: {f['nif']} - {f.get('advertencia_nif', 'NIF inválido')}")
                    print()
            return
        
        parser.print_help()
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
