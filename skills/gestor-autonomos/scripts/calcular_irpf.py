#!/usr/bin/env python3
"""
Calculador de Pago Fraccionado IRPF (Modelo 130) para Autónomos en España
Método de Estimación Directa Simplificada.
Usa Decimal para precisión monetaria exacta.
"""

import argparse
from decimal import Decimal, ROUND_HALF_UP
import json
import sys
from datetime import datetime

# Constantes fiscales 2024-2025
PORCENTAJE_PAGO_FRACCIONADO = Decimal('20')  # 20% del rendimiento neto
REDUCCION_GASTOS_DIFICIL_JUSTIFICACION = Decimal('7')  # 7% para estimación directa simplificada (máx 2000€)
MAXIMO_REDUCCION_GASTOS = Decimal('2000')

def redondear_centimos(valor: Decimal) -> Decimal:
    """Redondea a 2 decimales según norma fiscal española."""
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calcular_modelo_130(
    ingresos_trimestre: Decimal,
    gastos_trimestre: Decimal,
    retenciones_trimestre: Decimal = Decimal('0'),
    ingresos_acumulados_anteriores: Decimal = Decimal('0'),
    gastos_acumulados_anteriores: Decimal = Decimal('0'),
    retenciones_acumuladas_anteriores: Decimal = Decimal('0'),
    pagos_fraccionados_anteriores: Decimal = Decimal('0'),
    aplicar_reduccion_5_gastos: bool = True
) -> dict:
    """
    Calcula el pago fraccionado de IRPF (Modelo 130).
    
    El modelo 130 calcula el 20% del rendimiento neto ACUMULADO en el año,
    menos las retenciones y pagos fraccionados ya realizados.
    
    Args:
        ingresos_trimestre: Ingresos del trimestre actual (sin IVA)
        gastos_trimestre: Gastos deducibles del trimestre (sin IVA)
        retenciones_trimestre: Retenciones practicadas en el trimestre
        ingresos_acumulados_anteriores: Suma de ingresos de trimestres anteriores del año
        gastos_acumulados_anteriores: Suma de gastos de trimestres anteriores del año
        retenciones_acumuladas_anteriores: Suma de retenciones de trimestres anteriores
        pagos_fraccionados_anteriores: Suma de pagos modelo 130 de trimestres anteriores
        aplicar_reduccion_5_gastos: Aplicar reducción del 7% por gastos de difícil justificación
    
    Returns:
        Diccionario con desglose completo del cálculo
    """
    # Calcular totales acumulados del año
    ingresos_acumulados = ingresos_trimestre + ingresos_acumulados_anteriores
    gastos_acumulados = gastos_trimestre + gastos_acumulados_anteriores
    retenciones_acumuladas = retenciones_trimestre + retenciones_acumuladas_anteriores
    
    # Rendimiento neto previo
    rendimiento_neto_previo = ingresos_acumulados - gastos_acumulados
    
    # Aplicar reducción por gastos de difícil justificación (7% de rendimiento neto, máx 2000€)
    reduccion_gastos = Decimal('0')
    if aplicar_reduccion_5_gastos and rendimiento_neto_previo > 0:
        reduccion_gastos = rendimiento_neto_previo * REDUCCION_GASTOS_DIFICIL_JUSTIFICACION / Decimal('100')
        reduccion_gastos = min(reduccion_gastos, MAXIMO_REDUCCION_GASTOS)
        reduccion_gastos = redondear_centimos(reduccion_gastos)
    
    # Rendimiento neto
    rendimiento_neto = rendimiento_neto_previo - reduccion_gastos
    rendimiento_neto = redondear_centimos(rendimiento_neto)
    
    # Calcular 20% del rendimiento neto acumulado
    pago_20_por_ciento = Decimal('0')
    if rendimiento_neto > 0:
        pago_20_por_ciento = rendimiento_neto * PORCENTAJE_PAGO_FRACCIONADO / Decimal('100')
        pago_20_por_ciento = redondear_centimos(pago_20_por_ciento)
    
    # Deducir retenciones acumuladas
    resultado_tras_retenciones = pago_20_por_ciento - retenciones_acumuladas
    resultado_tras_retenciones = redondear_centimos(resultado_tras_retenciones)
    
    # Deducir pagos fraccionados anteriores del año
    resultado_final = resultado_tras_retenciones - pagos_fraccionados_anteriores
    resultado_final = redondear_centimos(resultado_final)
    
    # Si es negativo, se pone 0 (no se puede tener resultado negativo en modelo 130)
    resultado_a_ingresar = max(resultado_final, Decimal('0'))
    
    # Determinar tipo de resultado
    if resultado_a_ingresar > 0:
        resultado_tipo = "A INGRESAR"
    else:
        resultado_tipo = "SIN CUOTA"
    
    return {
        "trimestre": {
            "ingresos": str(ingresos_trimestre),
            "gastos": str(gastos_trimestre),
            "retenciones": str(retenciones_trimestre)
        },
        "acumulado_año": {
            "ingresos": str(ingresos_acumulados),
            "gastos": str(gastos_acumulados),
            "retenciones": str(retenciones_acumuladas)
        },
        "calculo": {
            "rendimiento_neto_previo": str(rendimiento_neto_previo),
            "reduccion_gastos_dificil_justificacion": str(reduccion_gastos),
            "rendimiento_neto": str(rendimiento_neto),
            "pago_20_por_ciento": str(pago_20_por_ciento),
            "menos_retenciones": str(retenciones_acumuladas),
            "menos_pagos_anteriores": str(pagos_fraccionados_anteriores),
            "resultado_previo": str(resultado_final)
        },
        "resultado_a_ingresar": str(resultado_a_ingresar),
        "resultado_tipo": resultado_tipo,
        "fecha_calculo": datetime.now().isoformat()
    }

def main():
    parser = argparse.ArgumentParser(
        description='Calculador de Pago Fraccionado IRPF (Modelo 130)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Primer trimestre del año:
  python3 calcular_irpf.py --ingresos 5000 --gastos 1500 --retenciones 750
  
  # Segundo trimestre (con acumulados):
  python3 calcular_irpf.py --ingresos 6000 --gastos 2000 --retenciones 900 \\
    --ingresos-anteriores 5000 --gastos-anteriores 1500 \\
    --retenciones-anteriores 750 --pagos-anteriores 400
  
  # Sin reducción por gastos de difícil justificación:
  python3 calcular_irpf.py --ingresos 5000 --gastos 1500 --sin-reduccion-gastos
        """
    )
    
    # Datos del trimestre actual
    parser.add_argument('--ingresos', type=str, required=True, help='Ingresos del trimestre (sin IVA)')
    parser.add_argument('--gastos', type=str, required=True, help='Gastos deducibles del trimestre (sin IVA)')
    parser.add_argument('--retenciones', type=str, default='0', help='Retenciones practicadas en el trimestre')
    
    # Acumulados de trimestres anteriores del año
    parser.add_argument('--ingresos-anteriores', type=str, default='0', help='Ingresos acumulados trimestres anteriores')
    parser.add_argument('--gastos-anteriores', type=str, default='0', help='Gastos acumulados trimestres anteriores')
    parser.add_argument('--retenciones-anteriores', type=str, default='0', help='Retenciones acumuladas anteriores')
    parser.add_argument('--pagos-anteriores', type=str, default='0', help='Pagos mod.130 anteriores del año')
    
    # Opciones
    parser.add_argument('--sin-reduccion-gastos', action='store_true', help='No aplicar reducción 7%% gastos difícil justificación')
    parser.add_argument('--json', action='store_true', help='Salida en formato JSON')
    
    args = parser.parse_args()
    
    try:
        resultado = calcular_modelo_130(
            ingresos_trimestre=Decimal(args.ingresos),
            gastos_trimestre=Decimal(args.gastos),
            retenciones_trimestre=Decimal(args.retenciones),
            ingresos_acumulados_anteriores=Decimal(args.ingresos_anteriores),
            gastos_acumulados_anteriores=Decimal(args.gastos_anteriores),
            retenciones_acumuladas_anteriores=Decimal(args.retenciones_anteriores),
            pagos_fraccionados_anteriores=Decimal(args.pagos_anteriores),
            aplicar_reduccion_5_gastos=not args.sin_reduccion_gastos
        )
        
        if args.json:
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        else:
            print("\n" + "="*55)
            print("   PAGO FRACCIONADO IRPF (MODELO 130)")
            print("="*55)
            
            print(f"\n📅 DATOS DEL TRIMESTRE:")
            print(f"   Ingresos:           {float(resultado['trimestre']['ingresos']):>12,.2f} €")
            print(f"   Gastos:             {float(resultado['trimestre']['gastos']):>12,.2f} €")
            print(f"   Retenciones:        {float(resultado['trimestre']['retenciones']):>12,.2f} €")
            
            print(f"\n📊 ACUMULADO AÑO:")
            print(f"   Ingresos:           {float(resultado['acumulado_año']['ingresos']):>12,.2f} €")
            print(f"   Gastos:             {float(resultado['acumulado_año']['gastos']):>12,.2f} €")
            print(f"   Retenciones:        {float(resultado['acumulado_año']['retenciones']):>12,.2f} €")
            
            print(f"\n🧮 CÁLCULO:")
            print(f"   Rdto. neto previo:  {float(resultado['calculo']['rendimiento_neto_previo']):>12,.2f} €")
            red_gastos = float(resultado['calculo']['reduccion_gastos_dificil_justificacion'])
            if red_gastos > 0:
                print(f"   Reducción 7%:       {red_gastos:>12,.2f} €")
            print(f"   Rendimiento neto:   {float(resultado['calculo']['rendimiento_neto']):>12,.2f} €")
            print(f"   20% rendimiento:    {float(resultado['calculo']['pago_20_por_ciento']):>12,.2f} €")
            print(f"   - Retenciones:      {float(resultado['calculo']['menos_retenciones']):>12,.2f} €")
            if float(resultado['calculo']['menos_pagos_anteriores']) > 0:
                print(f"   - Pagos anteriores: {float(resultado['calculo']['menos_pagos_anteriores']):>12,.2f} €")
            
            print("-"*55)
            cuota = float(resultado['resultado_a_ingresar'])
            if cuota > 0:
                print(f"   💰 A INGRESAR:      {cuota:>12,.2f} €")
            else:
                print(f"   ✅ SIN CUOTA:       {cuota:>12,.2f} €")
            print("="*55 + "\n")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
