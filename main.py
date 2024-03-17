import tkinter as tk
from PIL import Image, ImageTk
import ctypes

def vermenu():
    ventana2 = tk.Toplevel(ventana)
    ventana2.title("Menú")
    ventana2.geometry("400x300")
    etiqueta_menu = tk.Label(ventana2, text="Menú", font=("times new roman", 14))
    etiqueta_menu.pack(pady=20)

    def salir():
        ventana2.destroy()

    boton1 = tk.Button(ventana2, text="Salir", command=salir, font=("times new roman", 12), bg="Red", fg="black",
                       width=15, height=2, bd=12)
    boton1.pack(pady=5)

def salir():
    ventana.destroy()

user32 = ctypes.windll.user32
ancho_pantalla, alto_pantalla = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

ventana = tk.Tk()
ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")

imagen = Image.open("ank.png")
imagen = imagen.resize((ancho_pantalla, alto_pantalla))
imagen = ImageTk.PhotoImage(imagen)
fondo_label = tk.Label(ventana, image=imagen)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Obtener el tamaño de la imagen
ancho_imagen, alto_imagen = imagen.width(), imagen.height()

# Calcular las coordenadas para centrar los botones
x_centro = ancho_pantalla // 2
y_centro = alto_pantalla // 2

# Calcular el tamaño relativo de los botones
tamano_boton_x = 500
tamano_boton_y = 100

# Posicionar los botones en el centro
x_boton = x_centro - tamano_boton_x // 2
y_boton0 = y_centro - tamano_boton_y // 2 - 50
y_boton1 = y_centro - tamano_boton_y // 2 + 50

boton0 = tk.Button(ventana, text="Ver el menú", command=vermenu, font=("Comic Sans MS", 22), bg="Navy",
                   fg="white", width=15, height=2, bd=12)
boton0.place(x=x_boton, y=y_boton0, width=tamano_boton_x, height=tamano_boton_y)

boton1 = tk.Button(ventana, text="Salir", command=salir, font=("Comic Sans MS", 22), bg="Red", fg="black",
                   width=15, height=2, bd=12)
boton1.place(x=x_boton, y=y_boton1, width=tamano_boton_x, height=tamano_boton_y)

ventana.mainloop()
