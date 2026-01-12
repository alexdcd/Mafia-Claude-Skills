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

## Integración con Stripe/Substack

### ⚠️ IMPORTANTE - Diferencia entre Modelo 303 y Modelo 130

**Modelo 303 (IVA trimestral):**
- NO lleva base imponible en la presentación
- Solo reporta:
  - Casilla 03: Cuota IVA devengada (21% de clientes UE)
  - Casilla 60: Exportaciones exentas (base imponible de no-UE)

**Modelo 130 (IRPF trimestral):**
- SÍ lleva base imponible (suma de UE + no-UE)
- Luego resta gastos deducibles (fees)
- Resultado: rendimiento neto del trimestre

### IMPORTANTE - Reglas fiscales aplicadas

**1. El precio cobrado INCLUYE el IVA (Tax Inclusive)**
- El importe que cobras al cliente ya tiene el IVA dentro
- Para extraer la base imponible: `Base = Total / 1.21`
- NO multiplicar por 0.21 (eso sería añadir IVA encima)
- Ejemplo: Si cobras 60€ → Base = 49,59€, IVA = 10,41€

**2. La territorialidad se determina por PAÍS, no por moneda**
- Un cliente de Chile que paga en EUR → Exportación (sin IVA)
- Un cliente de España que paga en USD → Lleva IVA
- Prioridad: `country (billing)` > `country (ip)`

**3. Pagos sin país identificado → Criterio conservador (UE)**
- Si no hay país, se trata como cliente UE (paga IVA)
- Es más seguro fiscalmente aunque pagues algo más

**4. Los fees (Substack + Stripe) son gastos deducibles**
- Se restan en el IRPF (Modelo 130)
- NO afectan al IVA

### Formatos soportados

**CSV de Substack (formato nativo):**
```
email,date,currency,amount,Substack fee,Stripe fee,...,country (ip),country (billing)
user@mail.com,02-Oct-25,eur,€60.00,€6.00,€1.15,...,ES,ES
```

**CSV de Stripe Dashboard:**
```
id,Amount,Currency,Created (UTC),country (billing),Status,...
pi_xxx,60.00,eur,2025-10-02,ES,succeeded,...
```

### Uso del script

```bash
# Procesar CSV de Substack o Stripe:
python3 scripts/procesar_stripe.py --archivo pagos.csv --trimestre 4 --año 2025

# El script automáticamente:
# - Detecta formato (Substack o Stripe)
# - Parsea importes con símbolo (€60.00, CA$140.00)
# - Extrae base imponible dividiendo por 1.21 (no multiplicando)
# - Clasifica por PAÍS del cliente (no por moneda)
# - Calcula fees como gastos deducibles
```

### Resultados generados

**Para Modelo 303 (IVA):**
- Casilla 03: Cuota IVA a repercutir (21% de la base UE)
- Casilla 60: Exportaciones exentas (clientes no-UE) - IMPORTANTE: se reporta como base, no como cuota

**Para Modelo 130 (IRPF):**
- Base imponible: Suma de bases de clientes UE + no-UE
- Gastos: Fees de Substack + Stripe (deducibles)
- Rendimiento neto: Base imponible - Gastos

### Países UE-27 (referencia)

AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK

**⚠️ Reino Unido (GB/UK) NO está en la UE desde 2021 → Exento**

### Ejemplo práctico

```
Pago de 60€ desde España (ES):
  Base imponible: 60 / 1.21 = 49,59€
  IVA incluido:   60 - 49,59 = 10,41€

Pago de 60€ desde Chile (CL):
  Base imponible: 60€ (total, sin división)
  IVA: 0€ (exportación exenta)

Pago de 85€ sin país identificado:
  → Tratado como UE (conservador)
  Base imponible: 85 / 1.21 = 70,25€
  IVA incluido:   85 - 70,25 = 14,75€
```

## Consultas normativas

Para preguntas sobre legislación, consultar `references/normativa_fiscal.md` que contiene:
- Ley del IVA (Ley 37/1992)
- Ley del IRPF (Ley 35/2006)
- Reglamento de facturación
- Criterios de la AEAT
