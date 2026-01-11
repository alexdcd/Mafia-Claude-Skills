# 🎩 Mafia Claude Skills

Una colección de Claude Skills en español para potenciar tus flujos de trabajo con Claude AI.

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
- [¿Qué son las skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Usando skills en Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Cómo crear skills personalizadas](https://support.claude.com/en/articles/12512198-creating-custom-skills)

---

## 📋 Índice de Skills

| Skill | Descripción | Categoría |
|-------|-------------|-----------|
| [**Gestor Autónomos**](./skills/gestor-autonomos/) | Gestión contable y fiscal para autónomos en España. Cálculo de IVA, IRPF, procesamiento de Stripe/Substack. | 💼 Finanzas |

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
git clone https://github.com/tu-usuario/Mafia-Claude-Skills.git

# Añade la skill a tu proyecto
claude skill add ./Mafia-Claude-Skills/skills/gestor-autonomos
```

### Vía API de Claude

Incluye el contenido de la skill en el system prompt o como contexto adicional en tu llamada a la API.

---

## 📂 Estructura del Repositorio

```
Mafia-Claude-Skills/
├── skills/                    # Carpeta principal de skills
│   └── gestor-autonomos/      # Skill de gestión fiscal
│       ├── SKILL.md           # Instrucciones principales
│       ├── scripts/           # Scripts de Python
│       │   ├── calcular_iva.py
│       │   ├── calcular_irpf.py
│       │   ├── procesar_facturas.py
│       │   ├── procesar_stripe.py
│       │   └── generar_libro.py
│       └── references/        # Documentación de referencia
│           └── normativa_fiscal.md
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🔧 Skills Disponibles

### 💼 Gestor Autónomos España

> **Gestión contable y fiscal para trabajadores autónomos en España.**

Una skill completa para manejar la contabilidad y fiscalidad de autónomos con cálculos matemáticamente precisos.

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

➡️ [Ver documentación completa](./skills/gestor-autonomos/SKILL.md)

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este es un proyecto open source y nos encantaría que compartieras tus propias skills.

### Formas de contribuir:

1. **🐛 Reportar bugs**: Abre un [issue](https://github.com/tu-usuario/Mafia-Claude-Skills/issues) describiendo el problema
2. **💡 Sugerir mejoras**: Propón nuevas funcionalidades o skills
3. **🔧 Enviar Pull Requests**: Mejora skills existentes o añade nuevas
4. **📝 Mejorar documentación**: Ayuda a que las instrucciones sean más claras

### Cómo añadir una nueva skill:

```bash
# 1. Fork y clona el repo
git clone https://github.com/tu-usuario/Mafia-Claude-Skills.git

# 2. Crea una nueva carpeta para tu skill
mkdir -p skills/mi-nueva-skill

# 3. Añade los archivos requeridos
touch skills/mi-nueva-skill/SKILL.md

# 4. Crea un PR
```

Lee la [guía de contribución](CONTRIBUTING.md) para más detalles.

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
- [Awesome Claude Skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [Discord de Claude](https://discord.gg/anthropic)

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

[Reportar Bug](https://github.com/tu-usuario/Mafia-Claude-Skills/issues) · [Sugerir Skill](https://github.com/tu-usuario/Mafia-Claude-Skills/issues) · [Contribuir](CONTRIBUTING.md)

</div>
