#!/usr/bin/env python3
"""
Generador de Libro de Ingresos y Gastos para Autónomos en España.
Genera el libro obligatorio en formato CSV/JSON según normativa AEAT.
"""

import argparse
import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import List, Dict

def redondear_centimos(valor: Decimal) -> Decimal:
    """Redondea a 2 decimales."""
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def leer_facturas_csv(archivo: str) -> List[Dict]:
    """Lee facturas de un archivo CSV."""
    facturas = []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                facturas.append(row)
    except FileNotFoundError:
        print(f"Advertencia: Archivo no encontrado {archivo}", file=sys.stderr)
    return facturas

def procesar_factura(row: Dict, tipo: str) -> Dict:
    """Procesa una factura y calcula totales."""
    base = Decimal(row.get('base_imponible', '0').replace(',', '.'))
    iva_pct = Decimal(row.get('tipo_iva', '21').replace(',', '.'))
    ret_pct = Decimal(row.get('tipo_retencion', '0').replace(',', '.'))
    
    iva = redondear_centimos(base * iva_pct / Decimal('100'))
    retencion = redondear_centimos(base * ret_pct / Decimal('100'))
    total = redondear_centimos(base + iva - retencion)
    
    return {
        'tipo': tipo,
        'numero': row.get('numero', ''),
        'fecha': row.get('fecha', ''),
        'nif': row.get('nif', ''),
        'nombre': row.get('nombre', row.get('concepto', '')),
        'concepto': row.get('concepto', ''),
        'base_imponible': str(base),
        'tipo_iva': str(iva_pct),
        'cuota_iva': str(iva),
        'tipo_retencion': str(ret_pct),
        'retencion': str(retencion),
        'total': str(total)
    }

def generar_libro(
    trimestre: int,
    año: int,
    facturas_emitidas: str = None,
    facturas_recibidas: str = None
) -> Dict:
    """
    Genera el libro de ingresos y gastos.
    
    Args:
        trimestre: 1-4
        año: Año fiscal
        facturas_emitidas: Ruta CSV facturas emitidas
        facturas_recibidas: Ruta CSV facturas recibidas
    
    Returns:
        Libro completo con ingresos, gastos y resúmenes
    """
    libro = {
        'periodo': {
            'trimestre': trimestre,
            'año': año,
            'descripcion': f'{trimestre}T {año}'
        },
        'ingresos': [],
        'gastos': [],
        'resumen': {},
        'fecha_generacion': datetime.now().isoformat()
    }
    
    # Totales
    total_ingresos_base = Decimal('0')
    total_ingresos_iva = Decimal('0')
    total_ingresos_retencion = Decimal('0')
    total_gastos_base = Decimal('0')
    total_gastos_iva = Decimal('0')
    
    # Procesar facturas emitidas (ingresos)
    if facturas_emitidas:
        rows = leer_facturas_csv(facturas_emitidas)
        for row in rows:
            factura = procesar_factura(row, 'ingreso')
            libro['ingresos'].append(factura)
            total_ingresos_base += Decimal(factura['base_imponible'])
            total_ingresos_iva += Decimal(factura['cuota_iva'])
            total_ingresos_retencion += Decimal(factura['retencion'])
    
    # Procesar facturas recibidas (gastos)
    if facturas_recibidas:
        rows = leer_facturas_csv(facturas_recibidas)
        for row in rows:
            factura = procesar_factura(row, 'gasto')
            libro['gastos'].append(factura)
            total_gastos_base += Decimal(factura['base_imponible'])
            total_gastos_iva += Decimal(factura['cuota_iva'])
    
    # Calcular resúmenes
    libro['resumen'] = {
        'ingresos': {
            'num_facturas': len(libro['ingresos']),
            'base_imponible': str(redondear_centimos(total_ingresos_base)),
            'iva_repercutido': str(redondear_centimos(total_ingresos_iva)),
            'retenciones': str(redondear_centimos(total_ingresos_retencion))
        },
        'gastos': {
            'num_facturas': len(libro['gastos']),
            'base_imponible': str(redondear_centimos(total_gastos_base)),
            'iva_soportado': str(redondear_centimos(total_gastos_iva))
        },
        'liquidacion': {
            'rendimiento_neto': str(redondear_centimos(total_ingresos_base - total_gastos_base)),
            'iva_a_liquidar': str(redondear_centimos(total_ingresos_iva - total_gastos_iva))
        }
    }
    
    return libro

def exportar_csv(libro: Dict, archivo: str):
    """Exporta el libro a formato CSV."""
    with open(archivo, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Cabecera
        writer.writerow(['LIBRO DE INGRESOS Y GASTOS'])
        writer.writerow([f'Periodo: {libro["periodo"]["descripcion"]}'])
        writer.writerow([])
        
        # Ingresos
        writer.writerow(['=== INGRESOS (FACTURAS EMITIDAS) ==='])
        writer.writerow(['Número', 'Fecha', 'NIF', 'Concepto', 'Base Imponible', 'Tipo IVA', 'Cuota IVA', 'Retención', 'Total'])
        for f in libro['ingresos']:
            writer.writerow([
                f['numero'], f['fecha'], f['nif'], f['concepto'],
                f['base_imponible'], f['tipo_iva'], f['cuota_iva'],
                f['retencion'], f['total']
            ])
        writer.writerow([])
        
        # Gastos
        writer.writerow(['=== GASTOS (FACTURAS RECIBIDAS) ==='])
        writer.writerow(['Número', 'Fecha', 'NIF', 'Concepto', 'Base Imponible', 'Tipo IVA', 'Cuota IVA', 'Retención', 'Total'])
        for f in libro['gastos']:
            writer.writerow([
                f['numero'], f['fecha'], f['nif'], f['concepto'],
                f['base_imponible'], f['tipo_iva'], f['cuota_iva'],
                f['retencion'], f['total']
            ])
        writer.writerow([])
        
        # Resumen
        writer.writerow(['=== RESUMEN ==='])
        r = libro['resumen']
        writer.writerow(['Total ingresos (base)', r['ingresos']['base_imponible']])
        writer.writerow(['IVA repercutido', r['ingresos']['iva_repercutido']])
        writer.writerow(['Retenciones practicadas', r['ingresos']['retenciones']])
        writer.writerow(['Total gastos (base)', r['gastos']['base_imponible']])
        writer.writerow(['IVA soportado', r['gastos']['iva_soportado']])
        writer.writerow(['Rendimiento neto', r['liquidacion']['rendimiento_neto']])
        writer.writerow(['IVA a liquidar', r['liquidacion']['iva_a_liquidar']])

def main():
    parser = argparse.ArgumentParser(
        description='Generador de Libro de Ingresos y Gastos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Generar libro del 1er trimestre 2024:
  python3 generar_libro.py --trimestre 1 --año 2024 \\
    --facturas-emitidas emitidas.csv --facturas-recibidas recibidas.csv
  
  # Solo con facturas emitidas:
  python3 generar_libro.py --trimestre 2 --año 2024 --facturas-emitidas ventas.csv
  
  # Exportar a CSV:
  python3 generar_libro.py --trimestre 1 --año 2024 --facturas-emitidas f.csv --exportar libro.csv

Formato CSV esperado (con cabecera):
numero,fecha,nif,concepto,base_imponible,tipo_iva,tipo_retencion
        """
    )
    
    parser.add_argument('--trimestre', type=int, required=True, choices=[1, 2, 3, 4], help='Trimestre (1-4)')
    parser.add_argument('--año', type=int, required=True, help='Año fiscal')
    parser.add_argument('--facturas-emitidas', type=str, help='CSV de facturas emitidas')
    parser.add_argument('--facturas-recibidas', type=str, help='CSV de facturas recibidas')
    parser.add_argument('--exportar', type=str, help='Exportar a archivo CSV')
    parser.add_argument('--json', action='store_true', help='Salida en formato JSON')
    
    args = parser.parse_args()
    
    if not args.facturas_emitidas and not args.facturas_recibidas:
        parser.error("Debe proporcionar al menos --facturas-emitidas o --facturas-recibidas")
    
    try:
        libro = generar_libro(
            trimestre=args.trimestre,
            año=args.año,
            facturas_emitidas=args.facturas_emitidas,
            facturas_recibidas=args.facturas_recibidas
        )
        
        if args.exportar:
            exportar_csv(libro, args.exportar)
            print(f"\n✅ Libro exportado a: {args.exportar}\n")
        
        if args.json:
            print(json.dumps(libro, indent=2, ensure_ascii=False))
        elif not args.exportar:
            # Mostrar resumen en terminal
            print("\n" + "="*60)
            print(f"   LIBRO DE INGRESOS Y GASTOS - {libro['periodo']['descripcion']}")
            print("="*60)
            
            r = libro['resumen']
            
            print(f"\n📈 INGRESOS ({r['ingresos']['num_facturas']} facturas):")
            print(f"   Base imponible:     {float(r['ingresos']['base_imponible']):>12,.2f} €")
            print(f"   IVA repercutido:    {float(r['ingresos']['iva_repercutido']):>12,.2f} €")
            print(f"   Retenciones:        {float(r['ingresos']['retenciones']):>12,.2f} €")
            
            print(f"\n📉 GASTOS ({r['gastos']['num_facturas']} facturas):")
            print(f"   Base imponible:     {float(r['gastos']['base_imponible']):>12,.2f} €")
            print(f"   IVA soportado:      {float(r['gastos']['iva_soportado']):>12,.2f} €")
            
            print("\n" + "-"*60)
            print("📊 LIQUIDACIÓN:")
            rn = float(r['liquidacion']['rendimiento_neto'])
            iva = float(r['liquidacion']['iva_a_liquidar'])
            print(f"   Rendimiento neto:   {rn:>12,.2f} €")
            if iva >= 0:
                print(f"   IVA a ingresar:     {iva:>12,.2f} €")
            else:
                print(f"   IVA a compensar:    {iva:>12,.2f} €")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
