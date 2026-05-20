# 🎩 Mafia Claude Skills

Una colección de Claude Skills en español para potenciar tus flujos de trabajo con AI.

![Mafia Claude Skills](mafia_claude_skills.png)

[![Licencia](https://img.shields.io/badge/Licencia-Apache%202.0-blue.svg)](LICENSE)
[![Contribuciones Bienvenidas](https://img.shields.io/badge/Contribuciones-Bienvenidas-brightgreen.svg)](CONTRIBUTING.md)

---

## 📖 ¿Qué son las Claude Skills?

Las **Skills** son carpetas de instrucciones, scripts y recursos que Claude carga dinámicamente para mejorar su rendimiento en tareas especializadas. Una skill le enseña a Claude cómo completar tareas específicas de forma repetible y precisa.

Ejemplos de lo que pueden hacer las skills:
- 📊 Analizar datos siguiendo flujos de trabajo específicos
- 📝 Crear documentos con guías de estilo de tu empresa
- 🔢 Realizar cálculos precisos usando scripts de Python
- 🤖 Automatizar tareas personalizadas

**Más información oficial:**
- [¿Qué son las skills? Guía español](https://aimafia.substack.com/p/skills-ia)
- [Documentación skills oficial Claude](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Usando skills en Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Cómo crear skills personalizadas](https://support.claude.com/en/articles/12512198-creating-custom-skills)

---

## 📋 Índice de Skills

| Skill | Descripción | Categoría |
|-------|-------------|-----------|
| [**Gestor Autónomos**](./skills/gestor-autonomos/) | Gestión contable y fiscal para autónomos en España. Cálculo de IVA, IRPF, procesamiento de Stripe/Substack. | 💼 Finanzas |
| [**Landing Page Mastery**](./skills/landing-page-mastery/) | Sistema experto para crear y optimizar landing pages de alta conversión (SaaS, cursos, ebooks). | 🎨 Marketing |
| [**Vercel React Best Practices**](./skills/vercel-react-best-practices/) | Guías de optimización de rendimiento para React y Next.js mantenidas por Vercel. (Skill externa sincronizada) | ⚡ Desarrollo |
| [**Frontend Design**](./skills/frontend-design/) | Crea interfaces frontend distintivas y de grado de producción con alta calidad de diseño. (Skill de Anthropic) | 🎨 Diseño |
| [**Frontier Plan OpenCode Executor**](./skills/frontier-plan-opencode-executor/) | Ejecuta planes de implementación de IA frontera de forma segura y estructurada. *(Skill externa sincronizada)* | 🤖 Agentes |
| [**Agent Browser**](./skills/agent-browser/) | Automatización de navegador para interactuar con sitios web, extraer datos y testing. | 🌐 Web |
| [**Audio Transcriber**](./skills/audio-transcriber/) | Transforma grabaciones de audio en documentación Markdown con resúmenes. *(Source: community)* | 🎙️ Audio |
| [**Decision Toolkit**](./skills/decision-toolkit/) | Herramientas de toma de decisiones, guías paso a paso y exploración de escenarios. | 🧠 Productividad |
| [**Deep Research**](./skills/deep-research/) | Investigación profunda sobre cualquier tema con búsquedas web y análisis exhaustivo. | 🔍 Investigación |
| [**Fact Checker**](./skills/fact-checker/) | Verifica datos, hechos y afirmaciones para asegurar la veracidad de la información. | ✅ Verificación |
| [**File Organizer**](./skills/file-organizer/) | Organiza archivos, elimina duplicados y sugiere mejores estructuras de carpetas. | 📁 Utilidades |
| [**Find Skills**](./skills/find-skills/) | Descubre e instala nuevas agent skills respondiendo a las necesidades del usuario. | ⚙️ Utilidades |
| [**Frontend Slides**](./skills/frontend-slides/) | Crea presentaciones HTML animadas o convierte archivos PowerPoint. *(Source: ECC)* | 📊 Presentaciones |
| [**Humanizer**](./skills/humanizer/) | Transforma y humaniza el tono de los textos generados por IA para que suenen naturales. | ✍️ Redacción |
| [**MCP Builder**](./skills/mcp-builder/) | Guía para construir servidores MCP (Model Context Protocol) en Python y TypeScript. | 🛠️ Desarrollo |
| [**OpenRouter**](./skills/openrouter/) | Integración unificada con la API de OpenRouter para usar más de 400 modelos de IA. | 🔌 API |
| [**Process Interviewer**](./skills/process-interviewer/) | Entrevistador experto que extrae planes concretos de la mente del usuario antes de crear. | 📝 Planificación |
| [**Prompt Master**](./skills/prompt-master/) | Genera prompts ultra-optimizados para cualquier herramienta o modelo de IA. | 💬 Prompts |
| [**Repo First Defense**](./skills/repo-first-defense/) | Auditoría defensiva de seguridad para repositorios AI-native (dependencias, GitHub Actions, prompts, MCP). | 🛡️ Seguridad |


---

## 🚀 Cómo Usar las Skills

### En Claude.ai

1. Ve a **Configuración** → **Skills**
2. Haz clic en **"Añadir skill"**
3. Puedes:
   - **Subir manualmente**: Descarga la carpeta de la skill y súbela
   - **Desde URL**: Usa la URL del archivo `SKILL.md` en GitHub

### En Claude Code

```bash
# Clona el repositorio
git clone https://github.com/alexdcd/Mafia-Claude-Skills.git

# Añade la skill a tu proyecto
claude skill add ./Mafia-Claude-Skills/skills/gestor-autonomos
```

### Vía API de Claude

Incluye el contenido de la skill en el system prompt o como contexto adicional en tu llamada a la API.

---

## 📂 Estructura del Repositorio

```
Mafia-Claude-Skills/
├── .github/                   # Plantillas de Issues y Pull Requests
├── skills/                    # Carpeta principal que contiene todas las skills
│   ├── nombre-de-la-skill/    # Carpeta individual para cada skill
│   │   ├── SKILL.md           # Archivo obligatorio con instrucciones (YAML + Markdown)
│   │   ├── scripts/           # (Opcional) Scripts de apoyo (Python, etc.)
│   │   └── references/        # (Opcional) Documentación de referencia
├── README.md                  # Documentación principal
├── CONTRIBUTING.md            # Guía para colaboradores
└── LICENSE                    # Licencia del proyecto
```

---

## 🔧 Skills Disponibles

### 💼 Gestor Autónomos España

> **Gestión contable y fiscal para trabajadores autónomos en España.**

Una skill completa para manejar la contabilidad y fiscalidad de autónomos con cálculos matemáticamente precisos.

> [!CAUTION]
> **ADVERTENCIA**: Esta skill es una herramienta de apoyo y no sustituye el asesoramiento profesional. Los cálculos y sugerencias generados deben ser revisados por un gestor o profesional cualificado. El uso de esta herramienta se realiza bajo la responsabilidad exclusiva del usuario. Mafia Claude Skills y sus contribuidores no se hacen responsables de errores en las declaraciones fiscales o sanciones derivadas de su uso.

**Características:**

| Función | Descripción |
|---------|-------------|
| 📊 Modelo 303 (IVA) | Cálculo automático del IVA trimestral |
| 📈 Modelo 130 (IRPF) | Cálculo del pago fraccionado de IRPF |
| 🧾 Facturas | Procesamiento y validación de facturas |
| 💳 Stripe/Substack | Procesamiento de ingresos digitales |
| 📚 Libro contable | Generación del libro de ingresos/gastos |
| 📖 Normativa | Referencia de legislación fiscal española |

**Ejemplo de uso:**

```
Usuario: Necesito calcular el IVA del 3T 2024. 
         Facturé 12.000€ y tengo gastos deducibles por 3.500€.

Claude: [Usando Gestor Autónomos] Ejecutando cálculo...

📊 MODELO 303 - 3T 2024
━━━━━━━━━━━━━━━━━━━━━━
Base imponible:     12.000,00 €
IVA repercutido:     2.520,00 € (21%)

Gastos deducibles:   3.500,00 €
IVA soportado:         735,00 € (21%)

━━━━━━━━━━━━━━━━━━━━━━
💰 IVA A INGRESAR:   1.785,00 €

📅 Plazo: 1-20 Octubre 2024
```

**Estructura de la skill:**

```
gestor-autonomos/
├── SKILL.md           # Instrucciones y lógica fiscal
├── scripts/           # Lógica de cálculo en Python
│   ├── calcular_iva.py
│   ├── calcular_irpf.py
│   ├── procesar_facturas.py
│   ├── procesar_stripe.py
│   └── generar_libro.py
└── references/        # Documentación de la AEAT
    └── normativa_fiscal.md
```

➡️ [Ver documentación completa](./skills/gestor-autonomos/SKILL.md)

---

### 🎨 Landing Page Mastery

> **Sistema experto para crear y optimizar landing pages de alta conversión.**

Una skill diseñada para marketers y fundadores que necesitan crear páginas de venta efectivas o mejorar las existentes basándose en datos y psicología del usuario.

**Características:**

| Función | Descripción |
|---------|-------------|
| 🏗️ Estructuras | Plantillas probadas para SaaS, Cursos, Ebooks y Newsletters |
| ✍️ Copywriting | Generación de textos con frameworks (PAS, AIDA, STAR) |
| 🔍 Auditoría | Checklist de 100 puntos para optimizar conversiones |
| 🎨 Diseño | Guías de UX/UI, color y tipografía orientadas a conversión |
| 📊 Benchmarks | Comparativa con métricas de mercado (2026) |

**Casos de uso:**
- Crear una landing page desde cero para un nuevo SaaS.
- Auditar una página que no está convirtiendo bien.
- Redactar los textos de venta.

**Estructura de la skill:**

```
landing-page-mastery/
├── SKILL.md           # Instrucciones y flujos de trabajo
└── references/        # Base de conocimiento experta
    ├── structures.md      # Estructuras por tipo de producto
    ├── copywriting.md     # Fórmulas de redacción
    ├── design.md          # Guías visuales
    ├── audit-checklist.md # Auditoría paso a paso
    └── conversion-elements.md # Elementos de conversión
```

➡️ [Ver documentación completa](./skills/landing-page-mastery/SKILL.md)

---

### 🎨 Frontend Design

> **Crea interfaces frontend distintivas y de grado de producción con alta calidad de diseño.**

Una skill de Anthropic diseñada para guiar la creación de interfaces que eviten la estética genérica de la IA y apuesten por diseños audaces, memorables y refinados.

**Características:**

| Función | Descripción |
|---------|-------------|
| 🖋️ Tipografía | Selección de fuentes únicas y con carácter |
| 🎨 Color y Temas | Paletas cohesivas y acentos definidos |
| ✨ Animación | Micro-interacciones y movimientos de alto impacto |
| 📐 Composición | Layouts inesperados y uso creativo del espacio |
| 🌫️ Texturas | Fondos con profundidad y efectos visuales modernos |

**Cuando usar esta skill:**
- Al construir componentes web, landing pages o dashboards.
- Para "embellecer" una interfaz existente.
- Cuando buscas un diseño premium que no parezca generado por IA.

**Estructura de la skill:**

```
frontend-design/
├── SKILL.md           # Instrucciones y principios de diseño
└── LICENSE.txt        # Licencia Apache 2.0
```

➡️ [Ver documentación completa](./skills/frontend-design/SKILL.md)

---

### 🤖 Frontier Plan OpenCode Executor

> **Ejecuta planes de implementación de IA frontera de forma segura y estructurada en OpenCode.**

Una skill externa sincronizada para validar y ejecutar paso a paso planes complejos de modelos como Claude Opus, forzando la verificación continua contra el repositorio real.

**Características:**

| Función | Descripción |
|---------|-------------|
| 🔎 Validación | Verifica la realidad del repositorio antes de ejecutar |
| 🛡️ Seguridad | Previene comandos destructivos e instalaciones no deseadas |
| 🔄 Ejecución Paso a Paso | Fuerza al modelo a ejecutar de a un paso y verificar |
| 👀 Inspección de Diffs | Revisa el tamaño y alcance real de cada cambio |

**Cuando usar esta skill:**
- Al recibir un plan detallado de implementación de un modelo grande (ej. Claude Opus/GPT-5).
- Para obligar a modelos más pequeños a ejecutar de manera disciplinada y segura.

**Estructura de la skill:**

```
frontier-plan-opencode-executor/
├── SKILL.md           # Flujo de trabajo, verificaciones e instrucciones
└── README.md          # Documentación general de la skill
```

➡️ [Ver documentación completa](./skills/frontier-plan-opencode-executor/SKILL.md)

---

### 🌐 Agent Browser
> **Automatización de navegador para interactuar con sitios web y extraer datos.**

Interactúa con páginas web, rellena formularios, toma capturas de pantalla y realiza testing web de forma automatizada.
➡️ [Ver documentación completa](./skills/agent-browser/SKILL.md)

---

### 🎙️ Audio Transcriber
> **Transforma grabaciones en documentación Markdown profesional.** *(Source: community)*

Procesa audio para generar transcripciones estructuradas y resúmenes inteligentes mediante LLMs.
➡️ [Ver documentación completa](./skills/audio-transcriber/SKILL.md)

---

### 🧠 Decision Toolkit
> **Herramientas estructuradas para la toma de decisiones.**

Genera guías paso a paso, detectores de sesgos y exploradores de escenarios para analizar opciones importantes de manera sistemática.
➡️ [Ver documentación completa](./skills/decision-toolkit/SKILL.md)

---

### 🔍 Deep Research
> **Investigación exhaustiva sobre cualquier temática usando la API de Deep Research.**

Automatiza la mejora de prompts de búsqueda y ejecuta análisis profundos con acceso web.
➡️ [Ver documentación completa](./skills/deep-research/SKILL.md)

---

### ✅ Fact Checker
> **Verificador de hechos y afirmaciones.**

Comprueba datos e información para asegurar su veracidad y precisión antes de su publicación o uso.
➡️ [Ver documentación completa](./skills/fact-checker/SKILL.md)

---

### 📁 File Organizer
> **Organizador inteligente de archivos y directorios.**

Entiende el contexto de tus archivos, encuentra duplicados y sugiere estructuras ordenadas para tu espacio de trabajo digital.
➡️ [Ver documentación completa](./skills/file-organizer/SKILL.md)

---

### ⚙️ Find Skills
> **Descubrimiento e instalación de nuevas habilidades.**

Permite buscar e instalar skills dinámicamente cuando preguntas cómo hacer una tarea específica con agentes.
➡️ [Ver documentación completa](./skills/find-skills/SKILL.md)

---

### 📊 Frontend Slides
> **Creación de presentaciones HTML ricas en animaciones.** *(Source: ECC)*

Construye diapositivas desde cero o convierte presentaciones de PowerPoint a web con facilidad.
➡️ [Ver documentación completa](./skills/frontend-slides/SKILL.md)

---

### ✍️ Humanizer
> **Da un toque humano a tus textos.**

Ajusta y mejora el texto generado por IA para eliminar la "voz de robot" y hacerlo más cercano y natural.
➡️ [Ver documentación completa](./skills/humanizer/SKILL.md)

---

### 🛠️ MCP Builder
> **Guía para crear servidores Model Context Protocol (MCP) de alta calidad.**

Ayuda en el desarrollo de herramientas MCP con Python (FastMCP) o TypeScript/Node para integrar APIs externas con LLMs.
➡️ [Ver documentación completa](./skills/mcp-builder/SKILL.md)

---

### 🔌 OpenRouter
> **Acceso unificado a modelos de IA a través de OpenRouter.**

Interactúa con una enorme variedad de modelos (más de 400) integrando fácilmente la API de OpenRouter.
➡️ [Ver documentación completa](./skills/openrouter/SKILL.md)

---

### 📝 Process Interviewer
> **Entrevistador implacable para extraer y aterrizar planes.**

Antes de construir, este agente te entrevista para clarificar tus ideas, eliminar ambigüedades y generar un plan de acción robusto.
➡️ [Ver documentación completa](./skills/process-interviewer/SKILL.md)

---

### 💬 Prompt Master
> **Generador de prompts optimizados para cualquier herramienta de IA.**

Crea o adapta prompts perfectos para ChatGPT, Cursor, Midjourney, herramientas de vídeo y cualquier LLM o agente.
➡️ [Ver documentación completa](./skills/prompt-master/SKILL.md)

---

### 🛡️ Repo First Defense
> **Auditoría defensiva para repositorios AI-native.**

Audita y protege repositorios contra ataques de cadena de suministro (supply chain), prompt injection, secretos expuestos y malas configuraciones en GitHub Actions.
➡️ [Ver documentación completa](./skills/repo-first-defense/SKILL.md)

---


## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este es un proyecto open source y nos encantaría que compartieras tus propias skills.

### Formas de contribuir:

1. **🐛 Reportar bugs**: Abre un [issue](https://github.com/alexdcd/Mafia-Claude-Skills/issues) describiendo el problema
2. **💡 Sugerir mejoras**: Propón nuevas funcionalidades o skills
3. **🔧 Enviar Pull Requests**: Mejora skills existentes o añade nuevas
4. **📝 Mejorar documentación**: Ayuda a que las instrucciones sean más claras

### Cómo añadir una nueva skill:

```bash
# 1. Fork y clona el repo
git clone https://github.com/alexdcd/Mafia-Claude-Skills.git

# 2. Crea una nueva carpeta para tu skill
mkdir -p skills/mi-nueva-skill

# 3. Añade los archivos requeridos
touch skills/mi-nueva-skill/SKILL.md

# 4. Crea un PR
```

Lee la [guía de contribución](CONTRIBUTING.md) para más detalles.

### Cómo sincronizar skills externas:

Este repositorio incluye un sistema para sincronizar skills desde otros repositorios (como Vercel Best Practices).

1. **Configuración**: Las skills externas se definen en `data/external-skills.json`.
2. **Sincronización**: Para actualizar o instalar estas skills, ejecuta:

```bash
# Requiere Python 3
python3 scripts/sync_skills.py
```

Esto descargará la última versión de las skills definidas en el archivo JSON. Puedes usar este mecanismo para mantener tu repositorio actualizado con las mejores prácticas de la industria.

---

## 📏 Plantilla de Skill

Usa esta plantilla para crear nuevas skills:

```markdown
---
name: nombre-de-mi-skill
description: >
  Descripción clara de qué hace esta skill y cuándo usarla.
  Sé específico sobre los casos de uso.
---

# Nombre de Mi Skill

Descripción detallada de la skill y sus capacidades.

## Cuándo usar esta skill

- Caso de uso 1
- Caso de uso 2
- Caso de uso 3

## Instrucciones

[Instrucciones detalladas para Claude sobre cómo ejecutar esta skill]

## Ejemplos

[Ejemplos reales mostrando la skill en acción]
```

---

## 📚 Recursos

### Documentación oficial
- [Anthropic - Skills Repository](https://github.com/anthropics/skills)
- [Centro de ayuda de Claude](https://support.claude.com)
- [API de Claude](https://docs.anthropic.com)

### Comunidad
- [La Mafia IA](https://aimafia.substack.com/)

---

## 📄 Licencia

Este proyecto está licenciado bajo la [Licencia Apache 2.0](LICENSE).

Las skills incluidas son de uso libre para fines personales y comerciales, sujeto a los términos de la licencia.

---

## ✨ Creado por

**MAFIA IA** - Creando herramientas útiles para la comunidad hispanohablante de IA.

---

<div align="center">

**¿Te ha sido útil?** ⭐ Dale una estrella al repositorio

[Reportar Bug](https://github.com/alexdcd/Mafia-Claude-Skills/issues/new?template=bug-report.md) · [Sugerir Skill](https://github.com/alexdcd/Mafia-Claude-Skills/issues/new?template=nueva-skill.md) · [Contribuir](CONTRIBUTING.md)

</div>
