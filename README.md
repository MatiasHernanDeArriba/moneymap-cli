# MoneyMap CLI

**MoneyMap CLI** es una herramienta de línea de comandos (CLI) desarrollada en Python para **rastrear, categorizar, analizar y exportar gastos personales** de forma rápida, ligera y sin depender de hojas de cálculo pesadas ni servicios externos complejos.

> **Estado del proyecto:** En desarrollo activo (base inicial con `main.py` y `expenses.json`). Este documento define la visión, el diseño funcional y la hoja de ruta de lo que se va a construir.

---

## Tabla de contenidos

- [Motivación y propósito](#motivación-y-propósito)
- [Funcionalidades planificadas](#funcionalidades-planificadas)
- [Arquitectura y estructura del proyecto](#arquitectura-y-estructura-del-proyecto)
- [Formato de datos (`expenses.json`)](#formato-de-datos-expensesjson)
- [Ejemplos de uso previstos](#ejemplos-de-uso-previstos)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Hoja de ruta (Roadmap)](#hoja-de-ruta-roadmap)
- [Contribuciones y licencia](#contribuciones-y-licencia)

---

## Motivación y propósito

Llevar un control constante de los gastos diarios suele fallar cuando el proceso exige abrir aplicaciones lentas, completar demasiados campos o depender de plataformas cerradas. **MoneyMap CLI** busca resolver eso ofreciendo un flujo directo desde la terminal:

- **Rapidez desde el teclado:** Registrar un gasto en segundos sin salir del entorno de trabajo.
- **Datos locales y transparentes:** Guardar la información en un archivo JSON legible (`expenses.json`) que el usuario pueda respaldar, versionar o inspeccionar fácilmente.
- **Claridad financiera:** Agrupar movimientos por categoría, periodo o método de pago para entender en qué se va el dinero.
- **Portabilidad:** Poder exportar los registros a formatos estándar (como CSV o reportes resumidos) para analizarlos en otras herramientas cuando haga falta.

---

## Funcionalidades planificadas

A medida que evolucione el proyecto, el objetivo es incorporar los siguientes módulos y capacidades:

### 1. Registro y gestión de gastos
- **Alta de gastos:** Registrar monto, fecha, categoría, descripción breve y (opcionalmente) medio de pago o etiquetas.
- **Listado y consulta:** Ver movimientos recientes, filtrar por rango de fechas, categoría, monto mínimo/máximo o palabra clave.
- **Edición y eliminación:** Corregir errores de carga o borrar registros duplicados/inválidos de forma segura.

### 2. Categorización y organización
- **Categorías predefinidas y personalizadas:** Organizar gastos en rubros como *Comida*, *Transporte*, *Vivienda*, *Servicios*, *Salud*, *Ocio*, *Educación*, entre otros.
- **Resúmenes por categoría:** Calcular totales y porcentajes de participación de cada categoría dentro de un mes o periodo seleccionado.

### 3. Análisis y resúmenes financieros
- **Resumen mensual y por periodo:** Visualizar el gasto total, promedio diario y comparativas entre meses.
- **Alertas o presupuestos básicos (futuro):** Definir topes mensuales por categoría para detectar desvíos a tiempo.

### 4. Exportación de datos
- **Exportación a CSV:** Generar archivos `.csv` listos para abrir en Excel, Google Sheets o scripts de análisis.
- **Reportes legibles:** Exportar resúmenes en texto plano o Markdown para guardar registros periódicos.

---

## Arquitectura y estructura del proyecto

La estructura inicial y proyectada del repositorio es la siguiente:

```text
moneymap-cli/
├── main.py          # Punto de entrada de la CLI, parseo de argumentos y orquestación
├── expenses.json    # Almacenamiento local de gastos (se crea/actualiza al registrar datos)
└── README.md        # Documentación general y planificación del proyecto
