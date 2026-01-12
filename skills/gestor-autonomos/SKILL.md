---
name: gestor-autonomos
description: >
  Gestoría y contabilidad para autónomos en España. Usar cuando el usuario 
  necesite calcular IVA trimestral (modelo 303), calcular pagos fraccionados 
  de IRPF (modelo 130), gestionar libro de ingresos y gastos, verificar 
  facturas emitidas o recibidas, calcular retenciones, preparar declaraciones 
  trimestrales, estimar impuestos a pagar, procesar ingresos de Stripe o 
  Substack (separando pagos UE con IVA vs pagos internacionales exentos, 
  convirtiendo monedas a euros), o cualquier consulta sobre fiscalidad o 
  contabilidad de autónomos en España. Este skill garantiza cálculos 
  matemáticamente precisos usando scripts de Python y aplica la normativa 
  fiscal española vigente.
---

# Gestor de Autónomos España

Skill para gestión contable y fiscal de trabajadores autónomos en España con cálculos matemáticamente precisos.

> [!CAUTION]
> **ADVERTENCIA**: Esta skill es una herramienta de apoyo y no sustituye el asesoramiento profesional. Los cálculos y sugerencias generados deben ser revisados por un gestor o profesional cualificado. El uso de esta herramienta se realiza bajo la responsabilidad exclusiva del usuario. Mafia Claude Skills y sus contribuidores no se hacen responsables de errores en las declaraciones fiscales o sanciones derivadas de su uso.

## Principios fundamentales

1. **Precisión matemática obligatoria**: SIEMPRE usar los scripts de Python para cualquier cálculo. NUNCA calcular mentalmente.
2. **Base legal**: Todas las operaciones siguen la normativa de la AEAT (Agencia Tributaria).
3. **Verificación doble**: Cada cálculo debe ser verificable y trazable.

## Workflow principal

### Paso 1: Identificar el tipo de operación

**¿Qué necesita el usuario?**
- Calcular IVA trimestral → Ejecutar `scripts/calcular_iva.py`
- Calcular IRPF trimestral → Ejecutar `scripts/calcular_irpf.py`
- Procesar facturas/gastos → Ejecutar `scripts/procesar_facturas.py`
- Generar libro contable → Ejecutar `scripts/generar_libro.py`
- **Procesar ingresos Stripe/Substack** → Ejecutar `scripts/procesar_stripe.py`
- Consulta normativa → Ver `references/normativa_fiscal.md`

### Paso 2: Recopilar datos

Solicitar al usuario la información necesaria según la operación:

**Para IVA trimestral:**
- Facturas emitidas (base imponible + IVA repercutido)
- Facturas recibidas deducibles (base imponible + IVA soportado)
- Trimestre (1T, 2T, 3T, 4T) y año

**Para IRPF (Modelo 130):**
- Ingresos del trimestre (sin IVA)
- Gastos deducibles del trimestre (sin IVA)
- Retenciones practicadas por clientes
- Pagos fraccionados anteriores del año

**Para facturas:**
- Número de factura
- Fecha
- NIF/CIF del cliente/proveedor
- Concepto
- Base imponible
- Tipo de IVA aplicable
- Retención IRPF (si aplica)

### Paso 3: Ejecutar cálculos con scripts

OBLIGATORIO usar scripts para todos los cálculos numéricos:

```bash
# Calcular IVA trimestral
python3 scripts/calcular_iva.py --iva-repercutido <cantidad> --iva-soportado <cantidad>

# Calcular IRPF modelo 130
python3 scripts/calcular_irpf.py --ingresos <cantidad> --gastos <cantidad> --retenciones <cantidad> --pagos-anteriores <cantidad>

# Procesar lista de facturas desde CSV
python3 scripts/procesar_facturas.py --archivo <ruta.csv> --tipo <emitidas|recibidas>

# Generar libro de ingresos y gastos
python3 scripts/generar_libro.py --trimestre <1-4> --año <YYYY> --facturas-emitidas <ruta> --facturas-recibidas <ruta>
```

### Paso 4: Presentar resultados

Mostrar al usuario:
1. Desglose completo del cálculo
2. Resultado final con formato monetario (€)
3. Fecha límite de presentación si aplica
4. Advertencias o consideraciones relevantes

## Tipos de IVA en España (2024-2025)

| Tipo | Porcentaje | Aplicación |
|------|------------|------------|
| General | 21% | Mayoría de bienes y servicios |
| Reducido | 10% | Alimentos, transporte, hostelería |
| Superreducido | 4% | Pan, leche, frutas, verduras, libros, prensa |
| Exento | 0% | Sanidad, educación, seguros, servicios financieros |

## Retenciones IRPF en facturas

| Situación | Retención |
|-----------|-----------|
| Profesionales (general) | 15% |
| Nuevos autónomos (primeros 3 años) | 7% |
| Cursos, conferencias | 15% |
| Arrendamientos | 19% |

## Plazos de presentación trimestral

| Trimestre | Período | Plazo presentación |
|-----------|---------|-------------------|
| 1T | Enero-Marzo | 1-20 Abril |
| 2T | Abril-Junio | 1-20 Julio |
| 3T | Julio-Septiembre | 1-20 Octubre |
| 4T | Octubre-Diciembre | 1-30 Enero (año siguiente) |

## Gastos deducibles principales

Ver detalle completo en `references/normativa_fiscal.md`

**Deducibles al 100%:**
- Cuota de autónomos
- Gestoría y asesoría
- Seguros de responsabilidad civil
- Material de oficina
- Hosting, dominios, software
- Formación relacionada con actividad
- Publicidad y marketing

**Deducibles con límites:**
- Suministros (30% si trabajas desde casa)
- Vehículo (50% máximo, según uso profesional)
- Dietas y desplazamientos (con límites diarios)

## Advertencias importantes

1. **Nunca aproximar**: Los cálculos fiscales deben ser exactos al céntimo.
2. **Conservar justificantes**: Obligatorio guardar facturas 4 años mínimo.
3. **Verificar NIFs**: Siempre validar que los NIFs/CIFs sean correctos.
4. **Coherencia IVA**: El IVA soportado solo es deducible si está vinculado a la actividad.

## Integración con Stripe (Substack, etc.)

Para procesar ingresos de plataformas como Substack que usan Stripe:

### Paso 1: Obtener datos de Stripe

**Opción A - Con MCP Stripe conectado:**
Usar el conector MCP de Stripe para listar charges del trimestre:
```
Listar todos los charges de Stripe de los últimos 3 meses
```

**Opción B - Exportar CSV desde Stripe Dashboard:**
1. Ir a Stripe Dashboard → Payments
2. Filtrar por fechas del trimestre
3. Exportar a CSV

### Paso 2: Procesar con el script

```bash
# Desde CSV exportado:
python3 scripts/procesar_stripe.py --archivo pagos.csv --trimestre 4 --año 2024

# Desde JSON (MCP):
python3 scripts/procesar_stripe.py --archivo charges.json --trimestre 4 --año 2024 --formato json

# Con tipos de cambio específicos:
python3 scripts/procesar_stripe.py --archivo pagos.csv --trimestre 1 --año 2025 --tipo-cambio USD:0.93
```

### Paso 3: Interpretar resultados

El script genera:

**Para Modelo 303 (IVA):**
- `base_imponible_ue`: Ingresos de clientes UE (casilla 01)
- `iva_repercutido_ue`: IVA 21% a declarar (casilla 03)
- `exportaciones_no_ue`: Van a casilla 60 (exentas)

**Para Modelo 130 (IRPF):**
- `ingresos_trimestre`: Total de ingresos (UE + no-UE)

### Tratamiento fiscal de ingresos Stripe/Substack

**Pagos desde la UE:**
- Requieren IVA del 21%
- Si Substack no lo cobra, TÚ debes declararlo
- Base imponible = importe recibido
- IVA = base × 21%

**Pagos desde fuera de la UE:**
- Exentos de IVA (exportación de servicios)
- Art. 21.2 Ley IVA: servicios a no establecidos en UE
- Declarar en casilla 60 del modelo 303

**Conversión de monedas:**
- Usar tipo de cambio del BCE del día del pago
- O tipo medio del trimestre (más práctico)
- El script obtiene tipos actuales automáticamente

### Países de la UE (referencia)

AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK

**Nota:** Reino Unido (GB) ya NO está en la UE desde 2021.

## Consultas normativas

Para preguntas sobre legislación, consultar `references/normativa_fiscal.md` que contiene:
- Ley del IVA (Ley 37/1992)
- Ley del IRPF (Ley 35/2006)
- Reglamento de facturación
- Criterios de la AEAT
