# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a Mafia Claude Skills! Este documento te guiará en cómo participar en el proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Crear una Nueva Skill](#crear-una-nueva-skill)
- [Estructura de una Skill](#estructura-de-una-skill)
- [Buenas Prácticas](#buenas-prácticas)
- [Pull Requests](#pull-requests)

---

## 📜 Código de Conducta

Este proyecto sigue un código de conducta basado en el respeto mutuo:

- Sé respetuoso y constructivo
- Acepta críticas de forma positiva
- Enfócate en lo mejor para la comunidad
- Usa un lenguaje inclusivo

---

## 🛠️ Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no haya sido reportado previamente
2. Abre un [Issue](https://github.com/tu-usuario/Mafia-Claude-Skills/issues/new)
3. Incluye:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Capturas de pantalla si aplica

### Sugerir Mejoras

1. Abre un Issue con la etiqueta `enhancement`
2. Describe la mejora propuesta
3. Explica por qué sería útil

### Contribuir Código

1. Fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-skill`)
3. Commit de tus cambios (`git commit -m 'Añadir nueva skill X'`)
4. Push a la rama (`git push origin feature/nueva-skill`)
5. Abre un Pull Request

---

## ✨ Crear una Nueva Skill

### Paso 1: Crea la estructura

```bash
mkdir -p skills/mi-skill-nombre
touch skills/mi-skill-nombre/SKILL.md
```

### Paso 2: Completa el SKILL.md

Usa esta plantilla mínima:

```markdown
---
name: mi-skill-nombre
description: >
  Descripción clara y completa de qué hace esta skill.
  Incluye cuándo se debe activar/usar.
---

# Nombre de la Skill

Descripción detallada.

## Cuándo Usar Esta Skill

- Caso de uso 1
- Caso de uso 2

## Instrucciones

[Instrucciones paso a paso para Claude]

## Ejemplos

[Ejemplos de uso real]
```

### Paso 3: Añade recursos opcionales

```
mi-skill-nombre/
├── SKILL.md           # ✅ Requerido
├── scripts/           # Opcional: scripts de ayuda
├── templates/         # Opcional: plantillas
└── references/        # Opcional: documentación de referencia
```

### Paso 4: Actualiza el README

Añade tu skill a la tabla en el README principal.

---

## 📐 Estructura de una Skill

### Archivo SKILL.md

El archivo `SKILL.md` es el corazón de cada skill. Contiene:

1. **Frontmatter YAML** (requerido):
   ```yaml
   ---
   name: nombre-en-minusculas-con-guiones
   description: >
     Descripción completa en una o más líneas.
   ---
   ```

2. **Contenido Markdown**:
   - Título y descripción
   - Cuándo usar la skill
   - Instrucciones detalladas para Claude
   - Ejemplos de uso
   - Referencias adicionales

### Scripts

Si tu skill necesita cálculos precisos o procesamiento de datos:

- Usa **Python 3** para scripts
- Incluye `#!/usr/bin/env python3` al inicio
- Usa `argparse` para argumentos de CLI
- Incluye docstrings y comentarios
- Soporta salida en JSON (`--json`) para integración

### Referencias

Para documentación de apoyo:

- Usa **Markdown**
- Incluye fuentes oficiales
- Mantén la información actualizada

---

## ✅ Buenas Prácticas

### Para el SKILL.md

| ✅ Hacer | ❌ Evitar |
|----------|-----------|
| Instrucciones claras y paso a paso | Instrucciones vagas |
| Ejemplos concretos | Solo teoría |
| Cobertura de casos edge | Asumir entrada perfecta |
| Escribir para Claude, no usuarios finales | Mezclar audiencias |
| Documentar dependencias | Asumir configuración previa |

### Para Scripts

```python
# ✅ Bueno: Usa Decimal para dinero
from decimal import Decimal
precio = Decimal('19.99')

# ❌ Malo: Float para dinero
precio = 19.99
```

```python
# ✅ Bueno: Manejo de errores
try:
    resultado = procesar_datos(entrada)
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

# ❌ Malo: Sin manejo de errores
resultado = procesar_datos(entrada)
```

### Para Documentación

- Usa español claro y conciso
- Incluye tablas para información estructurada
- Usa emojis con moderación para mejorar legibilidad
- Mantén las líneas cortas (< 100 caracteres)

---

## 🔄 Pull Requests

### Antes de enviar

- [ ] El código está probado y funciona
- [ ] SKILL.md tiene frontmatter válido
- [ ] Ejemplos son realistas y funcionan
- [ ] README.md está actualizado (si añades skill)
- [ ] No hay información sensible (tokens, contraseñas)

### Proceso de revisión

1. Un mantenedor revisará tu PR
2. Puede haber comentarios o sugerencias
3. Haz los cambios necesarios
4. Una vez aprobado, se hará merge

### Convención de commits

```bash
# Para nuevas skills
git commit -m "feat(skill): añadir skill de gestión de facturas"

# Para mejoras
git commit -m "improve(gestor-autonomos): añadir soporte para modelo 390"

# Para bugs
git commit -m "fix(scripts): corregir cálculo de redondeo en IVA"

# Para documentación
git commit -m "docs: actualizar guía de contribución"
```

---

## ❓ Preguntas

Si tienes dudas:

1. Revisa los [Issues existentes](https://github.com/tu-usuario/Mafia-Claude-Skills/issues)
2. Abre un nuevo Issue con la etiqueta `question`
3. Sé específico sobre tu pregunta

---

## 🙏 Agradecimientos

Gracias a todos los que contribuyen a hacer este proyecto mejor. Tu tiempo y esfuerzo son muy apreciados.

---

*¿Primera vez contribuyendo a open source? ¡No te preocupes! Estamos aquí para ayudarte.*
