import tkinter as tk
from datetime import datetime
import math

class FlipClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip Clock")
        self.root.geometry("1311x600")
        self.root.configure(bg='#0a0a1a')
        
        # Crear canvas para el fondo con efecto borroso
        self.canvas = tk.Canvas(root, bg='#0a0a1a', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Variables para los módulos del reloj
        self.hour_module = None
        self.minute_module = None
        self.second_module = None
        self.am_pm_module = None  # Módulo para AM/PM en formato 12h
        
        # Variables para la fecha
        self.date_label = None
        
        # Formato de hora (True = 24h, False = 12h)
        self.format_24h = False  # Iniciar con formato de 12 horas
        
        # Botones de formato
        self.format_buttons = []
        
        # Bandera para evitar redibujado excesivo
        self.is_drawing = False
        
        # Dibujar todo inicialmente
        self.redraw_all()
        
        # Actualizar el reloj cada segundo
        self.update_clock()
        
    def get_canvas_size(self):
        """Obtiene el tamaño actual del canvas"""
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1 or height <= 1:
            width, height = 1311, 600
        return width, height
        
    def draw_background(self):
        """Dibuja un fondo degradado similar a la imagen"""
        width, height = self.get_canvas_size()
        
        # Crear degradado radial desde la esquina superior izquierda
        # Optimizado para mejor rendimiento
        steps = 30  # Reducido de 50 para mejor rendimiento
        for i in range(steps):
            # Calcular posición y tamaño del círculo
            progress = i / steps
            x_center = width * 0.2
            y_center = height * 0.2
            max_radius = math.sqrt(width**2 + height**2) * 0.8
            
            radius = max_radius * progress
            
            # Calcular color basado en la posición
            if progress < 0.3:
                # Zona cálida (naranja/rosa) cerca del centro
                r = int(255 * (1 - progress * 2))
                g = int(180 * (1 - progress * 1.5))
                b = int(150 * (1 - progress))
            else:
                # Zona fría (azul/verde azulado)
                local_progress = (progress - 0.3) / 0.7
                r = int(50 + local_progress * 30)
                g = int(150 + local_progress * 50)
                b = int(200 + local_progress * 55)
            
            # Ajustar opacidad (simulada con intensidad)
            intensity = 0.3 * (1 - progress * 0.7)
            r = min(255, int(r * intensity))
            g = min(255, int(g * intensity))
            b = min(255, int(b * intensity))
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Dibujar círculo
            self.canvas.create_oval(
                x_center - radius, y_center - radius,
                x_center + radius, y_center + radius,
                fill=color, outline='', width=0
            )
        
        # Agregar algunos círculos adicionales para más textura (reducidos)
        for i in range(6):
            x = width * (0.1 + (i % 3) * 0.3)
            y = height * (0.3 + (i // 3) * 0.3)
            radius = width * 0.25
            
            # Color azul/verde azulado
            r, g, b = 30, 100, 180
            intensity = 0.12
            color = f"#{int(r*intensity):02x}{int(g*intensity):02x}{int(b*intensity):02x}"
            
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=color, outline='', width=0
            )
    
    def create_clock_modules(self):
        """Crea los tres módulos del reloj flip"""
        width, height = self.get_canvas_size()
        
        # Posición central para los módulos (centrado vertical y horizontal)
        center_x = width / 2
        center_y = height / 2.5  # Ligeramente arriba del centro para dejar espacio para fecha y botones
        
        # Dimensiones de cada módulo (proporcionales al tamaño de la ventana)
        module_width = min(200, width * 0.22)
        module_height = min(250, height * 0.5)
        spacing = width * 0.04
        
        # Si está en formato 12h, ajustar el espaciado para incluir AM/PM
        if not self.format_24h:
            # Crear módulo de horas
            x1 = center_x - module_width - spacing - module_width/2 - spacing/2
            y1 = center_y - module_height/2
            x2 = x1 + module_width
            y2 = y1 + module_height
            self.hour_module = self.create_flip_module(x1, y1, x2, y2, "HOUR")
            
            # Crear módulo de minutos
            x1 = center_x - module_width/2
            y1 = center_y - module_height/2
            x2 = x1 + module_width
            y2 = y1 + module_height
            self.minute_module = self.create_flip_module(x1, y1, x2, y2, "MINUTE")
            
            # Crear módulo de segundos
            x1 = center_x + spacing + module_width/2
            y1 = center_y - module_height/2
            x2 = x1 + module_width
            y2 = y1 + module_height
            self.second_module = self.create_flip_module(x1, y1, x2, y2, "SECOND")
            
            # Crear módulo AM/PM (más pequeño)
            am_pm_width = module_width * 0.7
            am_pm_height = module_height * 0.6
            x1 = center_x + spacing + module_width/2 + spacing + module_width
            y1 = center_y - am_pm_height/2
            x2 = x1 + am_pm_width
            y2 = y1 + am_pm_height
            self.am_pm_module = self.create_flip_module(x1, y1, x2, y2, "AM/PM")
        else:
            # Formato 24h - sin módulo AM/PM
            # Crear módulo de horas
            x1 = center_x - module_width - spacing - module_width/2
            y1 = center_y - module_height/2
            x2 = x1 + module_width
            y2 = y1 + module_height
            self.hour_module = self.create_flip_module(x1, y1, x2, y2, "HOUR")
            
            # Crear módulo de minutos
            x1 = center_x - module_width/2
            y1 = center_y - module_height/2
            x2 = x1 + module_width
            y2 = y1 + module_height
            self.minute_module = self.create_flip_module(x1, y1, x2, y2, "MINUTE")
            
            # Crear módulo de segundos
            x1 = center_x + spacing + module_width/2
            y1 = center_y - module_height/2
            x2 = x1 + module_width
            y2 = y1 + module_height
            self.second_module = self.create_flip_module(x1, y1, x2, y2, "SECOND")
            
            self.am_pm_module = None
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        """Crea un rectángulo con esquinas redondeadas"""
        points = []
        # Esquina superior izquierda
        points.extend([x1 + radius, y1, x1 + radius, y1, x1, y1, x1, y1 + radius])
        # Esquina superior derecha
        points.extend([x2 - radius, y1, x2, y1, x2, y1 + radius])
        # Esquina inferior derecha
        points.extend([x2, y2 - radius, x2, y2, x2 - radius, y2])
        # Esquina inferior izquierda
        points.extend([x1, y2, x1, y2 - radius, x1 + radius, y2])
        
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def create_flip_module(self, x1, y1, x2, y2, label):
        """Crea un módulo individual del reloj flip"""
        radius = 8  # Radio de las esquinas redondeadas
        
        # Fondo del módulo (gris oscuro con esquinas redondeadas)
        # Usar rectángulo normal ya que tkinter no tiene soporte nativo para esquinas redondeadas
        # Simularemos con un rectángulo y círculos en las esquinas
        module_bg = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='#2a2a3e', outline='#1a1a1a', width=2
        )
        
        # Línea divisoria horizontal en el centro (simula la división del flip)
        center_y = (y1 + y2) / 2
        self.canvas.create_line(
            x1 + 5, center_y, x2 - 5, center_y,
            fill='#000000', width=3
        )
        
        # Sombra sutil en la parte superior
        self.canvas.create_line(
            x1, y1 + 2, x2, y1 + 2,
            fill='#1a1a1a', width=1
        )
        
        # Calcular tamaño de fuente basado en el tamaño del módulo
        # Si es AM/PM, usar fuente más pequeña para texto
        if label == "AM/PM":
            font_size = int((x2 - x1) * 0.25)
            font_size = max(24, min(48, font_size))
        else:
            font_size = int((x2 - x1) * 0.4)
            font_size = max(48, min(96, font_size))
        
        # Área para el número (se actualizará dinámicamente)
        number_text = self.canvas.create_text(
            (x1 + x2) / 2, center_y,
            text="00" if label != "AM/PM" else "AM", font=('Arial', font_size, 'bold'),
            fill='#ffffff', anchor='center'
        )
        
        # Calcular tamaño de fuente para la etiqueta
        label_font_size = int((x2 - x1) * 0.07)
        label_font_size = max(10, min(14, label_font_size))
        
        # Etiqueta debajo del módulo
        label_text = self.canvas.create_text(
            (x1 + x2) / 2, y2 + 15,
            text=label, font=('Arial', label_font_size, 'normal'),
            fill='#ffffff', anchor='center'
        )
        
        return {
            'bg': module_bg,
            'number': number_text,
            'label': label_text,
            'coords': (x1, y1, x2, y2)
        }
    
    def create_date_label(self):
        """Crea la etiqueta de fecha debajo del reloj"""
        width, height = self.get_canvas_size()
        
        # Calcular tamaño de fuente basado en el tamaño de la ventana
        font_size = int(width * 0.027)
        font_size = max(18, min(32, font_size))
        
        self.date_label = self.canvas.create_text(
            width / 2, height * 0.75,
            text="", font=('Arial', font_size, 'normal'),
            fill='#ffffff', anchor='center'
        )
    
    def create_format_buttons(self):
        """Crea los botones para cambiar entre formato 24h y 12h"""
        width, height = self.get_canvas_size()
        
        # Limpiar botones anteriores
        for btn_id in self.format_buttons:
            self.canvas.delete(btn_id)
        self.format_buttons = []
        
        # Posición de los botones (debajo de la fecha)
        button_y = height * 0.85
        button_width = 120
        button_height = 35
        spacing = 20
        
        # Botón 24 horas
        btn_24_x = width / 2 - button_width - spacing / 2
        btn_24_bg = self.canvas.create_rectangle(
            btn_24_x, button_y - button_height/2,
            btn_24_x + button_width, button_y + button_height/2,
            fill='#3a3a5e' if self.format_24h else '#2a2a3e',
            outline='#ffffff', width=2 if self.format_24h else 1,
            tags='btn_24h'
        )
        btn_24_text = self.canvas.create_text(
            btn_24_x + button_width/2, button_y,
            text="24 horas", font=('Arial', 12, 'bold' if self.format_24h else 'normal'),
            fill='#ffffff', anchor='center',
            tags='btn_24h'
        )
        self.format_buttons.extend([btn_24_bg, btn_24_text])
        
        # Botón 12 horas
        btn_12_x = width / 2 + spacing / 2
        btn_12_bg = self.canvas.create_rectangle(
            btn_12_x, button_y - button_height/2,
            btn_12_x + button_width, button_y + button_height/2,
            fill='#3a3a5e' if not self.format_24h else '#2a2a3e',
            outline='#ffffff', width=2 if not self.format_24h else 1,
            tags='btn_12h'
        )
        btn_12_text = self.canvas.create_text(
            btn_12_x + button_width/2, button_y,
            text="12 horas", font=('Arial', 12, 'bold' if not self.format_24h else 'normal'),
            fill='#ffffff', anchor='center',
            tags='btn_12h'
        )
        self.format_buttons.extend([btn_12_bg, btn_12_text])
        
        # Vincular eventos de clic y hover
        def on_enter_24(e):
            self.canvas.itemconfig(btn_24_bg, fill='#4a4a6e')
            self.root.config(cursor='hand2')
        
        def on_leave_24(e):
            self.canvas.itemconfig(btn_24_bg, fill='#3a3a5e' if self.format_24h else '#2a2a3e')
            self.root.config(cursor='')
        
        def on_enter_12(e):
            self.canvas.itemconfig(btn_12_bg, fill='#4a4a6e')
            self.root.config(cursor='hand2')
        
        def on_leave_12(e):
            self.canvas.itemconfig(btn_12_bg, fill='#3a3a5e' if not self.format_24h else '#2a2a3e')
            self.root.config(cursor='')
        
        self.canvas.tag_bind('btn_24h', '<Button-1>', lambda e: self.set_format_24h())
        self.canvas.tag_bind('btn_12h', '<Button-1>', lambda e: self.set_format_12h())
        self.canvas.tag_bind('btn_24h', '<Enter>', on_enter_24)
        self.canvas.tag_bind('btn_24h', '<Leave>', on_leave_24)
        self.canvas.tag_bind('btn_12h', '<Enter>', on_enter_12)
        self.canvas.tag_bind('btn_12h', '<Leave>', on_leave_12)
    
    def set_format_24h(self):
        """Cambia al formato de 24 horas"""
        if not self.format_24h:
            self.format_24h = True
            self.redraw_all()
    
    def set_format_12h(self):
        """Cambia al formato de 12 horas"""
        if self.format_24h:
            self.format_24h = False
            self.redraw_all()
    
    def redraw_all(self):
        """Redibuja todos los elementos del canvas"""
        if self.is_drawing:
            return
        self.is_drawing = True
        self.canvas.delete("all")
        self.draw_background()
        self.create_clock_modules()
        self.create_date_label()
        self.create_format_buttons()
        self.is_drawing = False
    
    def update_clock(self):
        """Actualiza el reloj y la fecha cada segundo"""
        now = datetime.now()
        
        # Actualizar minutos y segundos (iguales en ambos formatos)
        minute = str(now.minute).zfill(2)
        second = str(now.second).zfill(2)
        
        # Actualizar horas según el formato
        if self.format_24h:
            # Formato 24 horas
            hour = str(now.hour).zfill(2)
            am_pm = ""
        else:
            # Formato 12 horas
            hour_12 = now.hour % 12
            if hour_12 == 0:
                hour_12 = 12
            hour = str(hour_12).zfill(2)
            am_pm = "AM" if now.hour < 12 else "PM"
        
        # Actualizar los números en los módulos
        if self.hour_module:
            self.canvas.itemconfig(self.hour_module['number'], text=hour)
        if self.minute_module:
            self.canvas.itemconfig(self.minute_module['number'], text=minute)
        if self.second_module:
            self.canvas.itemconfig(self.second_module['number'], text=second)
        
        # Actualizar módulo AM/PM si está en formato 12h
        if not self.format_24h and self.am_pm_module:
            self.canvas.itemconfig(self.am_pm_module['number'], text=am_pm)
        
        # Actualizar la fecha
        # Formato: "Lunes, 15 de Enero de 2024"
        days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        day_name = days[now.weekday()]
        month_name = months[now.month - 1]
        date_str = f"{day_name}, {now.day} de {month_name} de {now.year}"
        
        if self.date_label:
            self.canvas.itemconfig(self.date_label, text=date_str)
        
        # Programar la próxima actualización
        self.root.after(1000, self.update_clock)
    
    def on_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        if event.widget == self.root:
            self.redraw_all()

def main():
    root = tk.Tk()
    app = FlipClockApp(root)
    
    # Vincular el evento de redimensionamiento
    root.bind('<Configure>', app.on_resize)
    
    root.mainloop()

if __name__ == "__main__":
    main()

