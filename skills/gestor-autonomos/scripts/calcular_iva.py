#!/usr/bin/env python3
"""
Calculador de IVA Trimestral (Modelo 303) para Autónomos en España
Usa Decimal para precisión monetaria exacta.
"""

import argparse
from decimal import Decimal, ROUND_HALF_UP
import json
import sys
from datetime import datetime

def redondear_centimos(valor: Decimal) -> Decimal:
    """Redondea a 2 decimales (céntimos) según norma fiscal española."""
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calcular_iva_trimestral(
    iva_repercutido: Decimal,
    iva_soportado: Decimal,
    compensacion_trimestres_anteriores: Decimal = Decimal('0')
) -> dict:
    """
    Calcula el resultado del IVA trimestral (Modelo 303).
    
    Args:
        iva_repercutido: IVA cobrado en facturas emitidas
        iva_soportado: IVA pagado en facturas recibidas deducibles
        compensacion_trimestres_anteriores: IVA negativo de trimestres anteriores a compensar
    
    Returns:
        Diccionario con desglose completo del cálculo
    """
    # Cálculo de la cuota diferencial
    cuota_diferencial = iva_repercutido - iva_soportado
    cuota_diferencial = redondear_centimos(cuota_diferencial)
    
    # Aplicar compensación de trimestres anteriores si hay cuota positiva
    cuota_resultado = cuota_diferencial
    compensacion_aplicada = Decimal('0')
    
    if cuota_diferencial > 0 and compensacion_trimestres_anteriores > 0:
        compensacion_aplicada = min(cuota_diferencial, compensacion_trimestres_anteriores)
        cuota_resultado = cuota_diferencial - compensacion_aplicada
    
    cuota_resultado = redondear_centimos(cuota_resultado)
    
    # Determinar resultado
    if cuota_resultado > 0:
        resultado_tipo = "A INGRESAR"
    elif cuota_resultado < 0:
        resultado_tipo = "A COMPENSAR/DEVOLVER"
    else:
        resultado_tipo = "SIN ACTIVIDAD"
    
    return {
        "iva_repercutido": str(iva_repercutido),
        "iva_soportado": str(iva_soportado),
        "cuota_diferencial": str(cuota_diferencial),
        "compensacion_anterior": str(compensacion_trimestres_anteriores),
        "compensacion_aplicada": str(compensacion_aplicada),
        "compensacion_pendiente": str(compensacion_trimestres_anteriores - compensacion_aplicada),
        "cuota_resultado": str(cuota_resultado),
        "resultado_tipo": resultado_tipo,
        "fecha_calculo": datetime.now().isoformat()
    }

def calcular_desde_bases(
    base_imponible_emitidas: Decimal,
    tipo_iva_emitidas: Decimal,
    base_imponible_recibidas: Decimal,
    tipo_iva_recibidas: Decimal
) -> dict:
    """
    Calcula IVA a partir de bases imponibles y tipos de IVA.
    """
    iva_repercutido = redondear_centimos(base_imponible_emitidas * tipo_iva_emitidas / Decimal('100'))
    iva_soportado = redondear_centimos(base_imponible_recibidas * tipo_iva_recibidas / Decimal('100'))
    
    resultado = calcular_iva_trimestral(iva_repercutido, iva_soportado)
    resultado["base_imponible_emitidas"] = str(base_imponible_emitidas)
    resultado["tipo_iva_emitidas"] = str(tipo_iva_emitidas)
    resultado["base_imponible_recibidas"] = str(base_imponible_recibidas)
    resultado["tipo_iva_recibidas"] = str(tipo_iva_recibidas)
    
    return resultado

def main():
    parser = argparse.ArgumentParser(
        description='Calculador de IVA Trimestral (Modelo 303)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Con IVA ya calculado:
  python3 calcular_iva.py --iva-repercutido 2100 --iva-soportado 840
  
  # Con bases imponibles:
  python3 calcular_iva.py --base-emitidas 10000 --tipo-emitidas 21 --base-recibidas 4000 --tipo-recibidas 21
  
  # Con compensación de trimestres anteriores:
  python3 calcular_iva.py --iva-repercutido 500 --iva-soportado 200 --compensacion 150
        """
    )
    
    # Opción 1: IVA directo
    parser.add_argument('--iva-repercutido', type=str, help='IVA repercutido (cobrado)')
    parser.add_argument('--iva-soportado', type=str, help='IVA soportado (pagado)')
    
    # Opción 2: Bases imponibles
    parser.add_argument('--base-emitidas', type=str, help='Base imponible facturas emitidas')
    parser.add_argument('--tipo-emitidas', type=str, default='21', help='Tipo IVA emitidas (default: 21)')
    parser.add_argument('--base-recibidas', type=str, help='Base imponible facturas recibidas')
    parser.add_argument('--tipo-recibidas', type=str, default='21', help='Tipo IVA recibidas (default: 21)')
    
    # Compensación
    parser.add_argument('--compensacion', type=str, default='0', help='IVA a compensar de trimestres anteriores')
    
    # Formato de salida
    parser.add_argument('--json', action='store_true', help='Salida en formato JSON')
    
    args = parser.parse_args()
    
    try:
        compensacion = Decimal(args.compensacion)
        
        # Determinar modo de cálculo
        if args.iva_repercutido is not None and args.iva_soportado is not None:
            resultado = calcular_iva_trimestral(
                Decimal(args.iva_repercutido),
                Decimal(args.iva_soportado),
                compensacion
            )
        elif args.base_emitidas is not None and args.base_recibidas is not None:
            resultado = calcular_desde_bases(
                Decimal(args.base_emitidas),
                Decimal(args.tipo_emitidas),
                Decimal(args.base_recibidas),
                Decimal(args.tipo_recibidas)
            )
            resultado["compensacion_anterior"] = str(compensacion)
        else:
            parser.error("Debe proporcionar --iva-repercutido y --iva-soportado, o --base-emitidas y --base-recibidas")
        
        if args.json:
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        else:
            print("\n" + "="*50)
            print("   CÁLCULO IVA TRIMESTRAL (MODELO 303)")
            print("="*50)
            if "base_imponible_emitidas" in resultado:
                print(f"\n📄 FACTURAS EMITIDAS:")
                print(f"   Base imponible:     {float(resultado['base_imponible_emitidas']):>12,.2f} €")
                print(f"   Tipo IVA:           {float(resultado['tipo_iva_emitidas']):>12,.0f} %")
            print(f"   IVA repercutido:    {float(resultado['iva_repercutido']):>12,.2f} €")
            
            if "base_imponible_recibidas" in resultado:
                print(f"\n📥 FACTURAS RECIBIDAS:")
                print(f"   Base imponible:     {float(resultado['base_imponible_recibidas']):>12,.2f} €")
                print(f"   Tipo IVA:           {float(resultado['tipo_iva_recibidas']):>12,.0f} %")
            print(f"   IVA soportado:      {float(resultado['iva_soportado']):>12,.2f} €")
            
            print(f"\n📊 LIQUIDACIÓN:")
            print(f"   Cuota diferencial:  {float(resultado['cuota_diferencial']):>12,.2f} €")
            
            if float(resultado['compensacion_anterior']) > 0:
                print(f"   Compensación ant.:  {float(resultado['compensacion_aplicada']):>12,.2f} €")
            
            print("-"*50)
            cuota = float(resultado['cuota_resultado'])
            if cuota >= 0:
                print(f"   💰 RESULTADO:       {cuota:>12,.2f} € ({resultado['resultado_tipo']})")
            else:
                print(f"   💚 RESULTADO:       {cuota:>12,.2f} € ({resultado['resultado_tipo']})")
            print("="*50 + "\n")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
