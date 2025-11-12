# Documentación Técnica - Flip Clock

## 📐 Especificaciones Técnicas

### Dimensiones de la Ventana
- **Ancho**: 1311 píxeles
- **Alto**: 600 píxeles
- **Ratio**: 2.185:1 (aproximadamente)

### Formato por Defecto
- **Formato de hora inicial**: 12 horas (AM/PM)
- **Idioma de fecha**: Español

## 🎨 Especificaciones de Diseño

### Colores Utilizados

#### Fondos
- **Ventana principal**: `#0a0a1a` (Negro azulado muy oscuro)
- **Módulos del reloj**: `#2a2a3e` (Gris azulado oscuro)
- **Borde de módulos**: `#1a1a1a` (Negro)
- **Línea divisoria**: `#000000` (Negro puro)

#### Texto
- **Números del reloj**: `#ffffff` (Blanco)
- **Etiquetas**: `#ffffff` (Blanco)
- **Fecha**: `#ffffff` (Blanco)

#### Botones
- **Botón activo**: `#3a3a5e` (Gris azulado medio)
- **Botón inactivo**: `#2a2a3e` (Gris azulado oscuro)
- **Botón hover**: `#4a4a6e` (Gris azulado claro)
- **Borde activo**: `#ffffff` (Blanco, grosor 2px)
- **Borde inactivo**: `#ffffff` (Blanco, grosor 1px)

#### Fondo Degradado
- **Zona cálida (superior izquierda)**:
  - Rojo: 255 → 0
  - Verde: 180 → 0
  - Azul: 150 → 0
- **Zona fría (resto)**:
  - Rojo: 50 → 80
  - Verde: 150 → 200
  - Azul: 200 → 255

### Tipografías

- **Fuente principal**: Arial
- **Tamaños**:
  - Números del reloj: 48-96px (adaptativo)
  - Números AM/PM: 24-48px (adaptativo)
  - Etiquetas de módulos: 10-14px (adaptativo)
  - Fecha: 18-32px (adaptativo)
  - Botones: 12px (fijo)

### Espaciado

- **Espaciado entre módulos**: 4% del ancho de la ventana
- **Espaciado entre botones**: 20px
- **Margen inferior de módulos**: 15px
- **Posición vertical del reloj**: 40% desde arriba (height / 2.5)
- **Posición vertical de la fecha**: 75% desde arriba
- **Posición vertical de los botones**: 85% desde arriba

## 🔧 Arquitectura del Código

### Estructura de Clases

```
FlipClockApp
│
├── Variables de instancia
│   ├── root (tk.Tk)
│   ├── canvas (tk.Canvas)
│   ├── hour_module (dict)
│   ├── minute_module (dict)
│   ├── second_module (dict)
│   ├── am_pm_module (dict | None)
│   ├── date_label (int - canvas id)
│   ├── format_24h (bool)
│   ├── format_buttons (list)
│   └── is_drawing (bool)
│
└── Métodos
    ├── __init__()
    ├── get_canvas_size()
    ├── draw_background()
    ├── create_clock_modules()
    ├── create_rounded_rectangle()
    ├── create_flip_module()
    ├── create_date_label()
    ├── create_format_buttons()
    ├── set_format_24h()
    ├── set_format_12h()
    ├── redraw_all()
    ├── update_clock()
    └── on_resize()
```

### Flujo de Ejecución

1. **Inicialización** (`__init__`):
   - Crea la ventana principal
   - Configura el canvas
   - Inicializa variables
   - Llama a `redraw_all()` para dibujar la interfaz inicial
   - Inicia el ciclo de actualización con `update_clock()`

2. **Dibujado Inicial** (`redraw_all`):
   - Dibuja el fondo (`draw_background`)
   - Crea los módulos del reloj (`create_clock_modules`)
   - Crea la etiqueta de fecha (`create_date_label`)
   - Crea los botones de formato (`create_format_buttons`)

3. **Actualización Continua** (`update_clock`):
   - Obtiene la hora actual del sistema
   - Convierte según el formato seleccionado
   - Actualiza los textos de los módulos
   - Actualiza la fecha
   - Programa la próxima actualización (1 segundo)

4. **Interacción del Usuario**:
   - Click en botón → `set_format_24h()` o `set_format_12h()`
   - Cambio de formato → `redraw_all()` para recrear la interfaz

5. **Redimensionamiento**:
   - Evento `<Configure>` → `on_resize()`
   - `on_resize()` → `redraw_all()` para ajustar todo

## 📊 Estructura de Datos

### Módulo del Reloj (dict)

```python
{
    'bg': int,           # ID del canvas para el fondo del módulo
    'number': int,        # ID del canvas para el texto del número
    'label': int,         # ID del canvas para la etiqueta
    'coords': tuple       # (x1, y1, x2, y2) - Coordenadas del módulo
}
```

### Botones de Formato (list)

Lista de IDs de elementos del canvas que componen los botones:
- `[btn_24_bg, btn_24_text, btn_12_bg, btn_12_text]`

## 🔄 Algoritmos

### Conversión de Hora 24h a 12h

```python
hour_12 = now.hour % 12
if hour_12 == 0:
    hour_12 = 12  # Las 00:xx y 12:xx se muestran como 12:xx
am_pm = "AM" if now.hour < 12 else "PM"
```

### Cálculo de Posición de Módulos (Formato 24h)

```
center_x = width / 2
center_y = height / 2.5

module_width = min(200, width * 0.22)
module_height = min(250, height * 0.5)
spacing = width * 0.04

hour_x1 = center_x - module_width - spacing - module_width/2
minute_x1 = center_x - module_width/2
second_x1 = center_x + spacing + module_width/2
```

### Cálculo de Posición de Módulos (Formato 12h)

Similar al formato 24h, pero con ajuste para el módulo AM/PM:
- Los módulos principales se desplazan ligeramente a la izquierda
- El módulo AM/PM se coloca a la derecha del módulo de segundos
- Tamaño del módulo AM/PM: 70% del ancho y 60% del alto de los otros módulos

### Degradado del Fondo

El fondo se crea mediante círculos superpuestos:

1. **Círculo principal degradado** (30 capas):
   - Radio crece desde 0 hasta 80% de la diagonal de la ventana
   - Color cambia según la posición:
     - Primeros 30%: Tonos cálidos (naranja/rosa)
     - Resto: Tonos fríos (azul/verde azulado)
   - Intensidad disminuye desde el centro hacia afuera

2. **Círculos de textura** (6 círculos):
   - Distribuidos en una cuadrícula 3x2
   - Color azul/verde azulado
   - Intensidad fija: 12%

## ⚡ Optimizaciones

### Rendimiento

1. **Redibujado Selectivo**:
   - El fondo solo se redibuja al iniciar o redimensionar
   - La actualización de la hora solo modifica el texto, no redibuja elementos

2. **Prevención de Redibujados Múltiples**:
   - Flag `is_drawing` previene redibujados simultáneos
   - Retorno temprano si ya se está dibujando

3. **Optimización del Fondo**:
   - Reducción de capas de 50 a 30 para mejor rendimiento
   - Reducción de círculos de textura de 10 a 6

### Memoria

- Los elementos del canvas se eliminan antes de crear nuevos (`canvas.delete("all")`)
- No se acumulan elementos obsoletos en memoria

## 🧪 Casos de Prueba

### Formato 24h
- ✅ Hora 00:00 → Muestra "00"
- ✅ Hora 12:00 → Muestra "12"
- ✅ Hora 23:59 → Muestra "23"
- ✅ No muestra módulo AM/PM

### Formato 12h
- ✅ Hora 00:00 → Muestra "12 AM"
- ✅ Hora 11:59 → Muestra "11 AM"
- ✅ Hora 12:00 → Muestra "12 PM"
- ✅ Hora 13:00 → Muestra "01 PM"
- ✅ Hora 23:59 → Muestra "11 PM"
- ✅ Muestra módulo AM/PM

### Fecha
- ✅ Formato correcto: "Día, Día de Mes de Año"
- ✅ Nombres en español
- ✅ Actualización diaria automática

### Interfaz
- ✅ Botones responden al clic
- ✅ Efecto hover funciona
- ✅ Cambio de formato actualiza la interfaz
- ✅ Redimensionamiento mantiene el centrado

## 🔍 Debugging

### Logs y Mensajes

La aplicación no incluye sistema de logging integrado. Para debugging:

1. **Agregar prints temporales**:
```python
print(f"Formato: {'24h' if self.format_24h else '12h'}")
print(f"Hora actual: {now.hour}:{now.minute}:{now.second}")
```

2. **Verificar dimensiones**:
```python
width, height = self.get_canvas_size()
print(f"Canvas size: {width}x{height}")
```

### Problemas Comunes

1. **Módulos no centrados**:
   - Verificar que `center_x = width / 2`
   - Verificar cálculos de posición

2. **Fondo no se dibuja**:
   - Verificar que `get_canvas_size()` retorna valores válidos
   - Verificar que el canvas esté visible

3. **Hora no se actualiza**:
   - Verificar que `update_clock()` se llame recursivamente
   - Verificar que `root.after()` esté funcionando

## 📦 Dependencias

### Librerías Estándar de Python

- **tkinter**: Interfaz gráfica
  - `tk.Tk`: Ventana principal
  - `tk.Canvas`: Superficie de dibujo
  
- **datetime**: Manejo de fecha y hora
  - `datetime.now()`: Obtiene fecha/hora actual
  - `datetime.weekday()`: Día de la semana (0=Lunes)
  - `datetime.hour`, `datetime.minute`, `datetime.second`: Componentes de tiempo
  - `datetime.day`, `datetime.month`, `datetime.year`: Componentes de fecha

- **math**: Operaciones matemáticas
  - `math.sqrt()`: Raíz cuadrada (para cálculo de radio del degradado)

## 🚀 Mejoras Futuras

### Posibles Extensiones

1. **Temas personalizables**:
   - Múltiples esquemas de color
   - Fondos intercambiables

2. **Configuración persistente**:
   - Guardar preferencia de formato
   - Guardar posición de ventana

3. **Alarmas y recordatorios**:
   - Sistema de alarmas
   - Notificaciones

4. **Múltiples zonas horarias**:
   - Mostrar hora de diferentes zonas
   - Selector de zona horaria

5. **Animaciones**:
   - Transición suave al cambiar formato
   - Efecto de "flip" real en los números

6. **Personalización avanzada**:
   - Tamaño de fuente ajustable
   - Opacidad del fondo
   - Mostrar/ocultar segundos

---

**Versión del documento**: 1.0  
**Última actualización**: 2024

