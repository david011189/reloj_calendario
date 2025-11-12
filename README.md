# Flip Clock - Aplicación de Escritorio

Una aplicación de escritorio moderna que muestra la fecha y hora actual del sistema usando un diseño de reloj flip digital elegante, inspirado en los clásicos relojes flip de los años 70.

## 📋 Descripción

Flip Clock es una aplicación de escritorio desarrollada en Python que presenta un reloj digital con diseño flip clock, mostrando la hora en formato de 24 o 12 horas, junto con la fecha actual del sistema. La aplicación cuenta con un fondo degradado con efecto borroso que simula un paisaje natural, creando una experiencia visual atractiva y relajante.

## ✨ Características

- **Diseño Flip Clock**: Módulos individuales para horas, minutos y segundos con estilo flip clock clásico
- **Formato de Hora Flexible**: 
  - Formato de 24 horas (00:00 - 23:59)
  - Formato de 12 horas (01:00 - 12:59) con indicador AM/PM
- **Fecha Completa**: Muestra la fecha actual en formato legible (ej: "Lunes, 15 de Enero de 2024")
- **Actualización en Tiempo Real**: La hora se actualiza cada segundo automáticamente
- **Interfaz Interactiva**: Botones para cambiar entre formatos de hora con efectos hover
- **Diseño Responsive**: Se adapta al tamaño de la ventana manteniendo el centrado
- **Fondo Artístico**: Degradado con efecto borroso que simula un paisaje natural

## 🖥️ Requisitos del Sistema

- **Sistema Operativo**: Windows 10 o superior
- **Python**: 3.7 o superior (solo para desarrollo)
- **Librerías**:
  - `tkinter` (incluida en Python estándar)
  - `datetime` (incluida en Python estándar)
  - `math` (incluida en Python estándar)

## 📦 Instalación

### Opción 1: Ejecutable (.exe)

1. Descarga el archivo `FlipClock.exe` desde la carpeta `dist/`
2. Ejecuta el archivo directamente (no requiere instalación de Python)

### Opción 2: Código Fuente

1. Clona o descarga el repositorio
2. Asegúrate de tener Python 3.7+ instalado
3. No se requieren dependencias adicionales (tkinter viene con Python)

## 🚀 Uso

### Ejecutar desde el código fuente:

```bash
python flip_clock_app.py
```

### Ejecutar el ejecutable:

Simplemente haz doble clic en `FlipClock.exe`

### Interfaz de Usuario:

- **Módulos del Reloj**: Muestran horas, minutos y segundos en la parte superior
- **Módulo AM/PM**: Aparece cuando se selecciona el formato de 12 horas
- **Fecha**: Se muestra debajo del reloj en formato completo
- **Botones de Formato**: 
  - "24 horas": Cambia al formato de 24 horas
  - "12 horas": Cambia al formato de 12 horas (formato por defecto)

## 🏗️ Estructura del Proyecto

```
Proyectos/05/
│
├── flip_clock_app.py      # Código fuente principal
├── README.md              # Documentación del proyecto
├── FlipClock.spec         # Archivo de configuración de PyInstaller
├── descripcion del proyecto.txt
│
├── dist/                  # Carpeta con el ejecutable
│   └── FlipClock.exe     # Ejecutable de la aplicación
│
└── build/                 # Archivos temporales de compilación
    └── FlipClock/
```

## 📚 Documentación del Código

### Clase Principal: `FlipClockApp`

#### Métodos Principales:

##### `__init__(self, root)`
Inicializa la aplicación, configura la ventana y comienza el ciclo de actualización.

**Parámetros:**
- `root`: Ventana principal de tkinter

**Configuración inicial:**
- Tamaño de ventana: 1311 x 600 píxeles
- Formato por defecto: 12 horas
- Fondo: Color oscuro (#0a0a1a)

##### `get_canvas_size(self)`
Obtiene las dimensiones actuales del canvas.

**Retorna:**
- `tuple`: (width, height) - Ancho y alto del canvas

##### `draw_background(self)`
Dibuja el fondo degradado con efecto borroso que simula un paisaje natural.

**Características:**
- Degradado radial desde la esquina superior izquierda
- Tonos cálidos (naranja/rosa) en la parte superior izquierda
- Tonos fríos (azul/verde azulado) en el resto
- Optimizado para rendimiento (30 capas)

##### `create_clock_modules(self)`
Crea los módulos del reloj flip (horas, minutos, segundos, y opcionalmente AM/PM).

**Comportamiento:**
- En formato 24h: Crea 3 módulos (HOUR, MINUTE, SECOND)
- En formato 12h: Crea 4 módulos (HOUR, MINUTE, SECOND, AM/PM)
- Los módulos se centran automáticamente según el formato

##### `create_flip_module(self, x1, y1, x2, y2, label)`
Crea un módulo individual del reloj flip.

**Parámetros:**
- `x1, y1`: Coordenadas superior izquierda
- `x2, y2`: Coordenadas inferior derecha
- `label`: Etiqueta del módulo ("HOUR", "MINUTE", "SECOND", "AM/PM")

**Retorna:**
- `dict`: Diccionario con referencias a los elementos del módulo

**Características del módulo:**
- Fondo gris oscuro (#2a2a3e)
- Línea divisoria horizontal en el centro
- Números en fuente grande y negrita
- Etiqueta debajo del módulo
- Tamaño de fuente adaptativo según el tamaño del módulo

##### `create_date_label(self)`
Crea la etiqueta que muestra la fecha actual.

**Formato de fecha:**
- "Día de la semana, Día de Mes de Año"
- Ejemplo: "Lunes, 15 de Enero de 2024"

##### `create_format_buttons(self)`
Crea los botones interactivos para cambiar entre formatos de hora.

**Características:**
- Dos botones: "24 horas" y "12 horas"
- Efecto hover (cambio de color y cursor)
- Botón activo resaltado con borde más grueso
- Centrados horizontalmente

##### `set_format_24h(self)`
Cambia el formato de hora a 24 horas.

##### `set_format_12h(self)`
Cambia el formato de hora a 12 horas.

##### `redraw_all(self)`
Redibuja todos los elementos del canvas.

**Uso:**
- Se llama cuando cambia el formato de hora
- Se llama cuando se redimensiona la ventana
- Previene redibujados múltiples simultáneos

##### `update_clock(self)`
Actualiza la hora y fecha cada segundo.

**Lógica de conversión:**
- **Formato 24h**: Muestra horas de 00 a 23
- **Formato 12h**: 
  - Convierte horas 0-11 a 12-11 (AM)
  - Convierte horas 12-23 a 12-11 (PM)
  - Muestra "AM" o "PM" según corresponda

**Actualización:**
- Se programa automáticamente cada 1000ms (1 segundo)

##### `on_resize(self, event)`
Maneja el evento de redimensionamiento de la ventana.

**Comportamiento:**
- Redibuja todos los elementos manteniendo el centrado
- Ajusta tamaños de fuente proporcionalmente

### Función Principal: `main()`

Crea la ventana principal y ejecuta el bucle de eventos de tkinter.

## 🔧 Compilación a Ejecutable (.exe)

Para generar el ejecutable, se utiliza PyInstaller:

### Requisitos:
```bash
pip install pyinstaller
```

### Comando de compilación:
```bash
pyinstaller --onefile --windowed --name "FlipClock" flip_clock_app.py
```

### Opciones utilizadas:
- `--onefile`: Crea un único archivo ejecutable
- `--windowed`: No muestra ventana de consola (solo interfaz gráfica)
- `--name "FlipClock"`: Nombre del ejecutable

### Resultado:
- El ejecutable se genera en la carpeta `dist/`
- Archivos temporales se guardan en `build/`
- Archivo de configuración: `FlipClock.spec`

## 🎨 Personalización

### Cambiar el tamaño de la ventana:

Edita la línea en `__init__`:
```python
self.root.geometry("1311x600")  # Cambia estos valores
```

### Cambiar el formato por defecto:

Edita la línea en `__init__`:
```python
self.format_24h = False  # True para 24h, False para 12h
```

### Cambiar colores:

Los colores principales están definidos en:
- Fondo de ventana: `#0a0a1a`
- Fondo de módulos: `#2a2a3e`
- Texto: `#ffffff`
- Botones activos: `#3a3a5e`
- Botones inactivos: `#2a2a3e`

## 🐛 Solución de Problemas

### La ventana no se muestra:
- Verifica que Python esté instalado correctamente
- Asegúrate de que tkinter esté disponible (viene con Python estándar)

### El reloj no se actualiza:
- Verifica que la fecha/hora del sistema esté correcta
- Reinicia la aplicación

### El ejecutable no funciona:
- Asegúrate de que el archivo esté completo
- Verifica que no esté bloqueado por el antivirus
- Ejecuta como administrador si es necesario

## 📝 Notas Técnicas

- **Rendimiento**: El fondo se dibuja una vez al iniciar y al redimensionar. La actualización de la hora solo modifica el texto, no redibuja todo.
- **Responsive**: Los elementos se ajustan proporcionalmente al tamaño de la ventana.
- **Centrado**: Todos los elementos están centrados horizontalmente usando `width / 2`.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## 👨‍💻 Autor

Desarrollado como proyecto de aplicación de escritorio con Python y tkinter.

## 🔄 Versión

**Versión actual**: 1.0

**Características principales**:
- Reloj flip digital
- Formato 24h/12h intercambiable
- Fecha completa en español
- Diseño responsive
- Ejecutable standalone

---

**Última actualización**: 11/11/2025


