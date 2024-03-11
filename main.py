import tkinter as tk

def mostrar_mensaje():
    pass

def cerrar_ventana():
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Marvel Comics")

# Crear un canvas para la imagen de fondo y los widgets
canvas = tk.Canvas(ventana)
canvas.pack(fill="both", expand=True)

# Crear un scrollbar
scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configurar el canvas para que se pueda desplazar
canvas.configure(yscrollcommand=scrollbar.set)

# Insertar la imagen de fondo en el canvas
imagen_fondo = tk.PhotoImage(file="ank.png")
canvas.create_image(0, 0, anchor="nw", image=imagen_fondo)

# Colocar otros widgets y contenido en el canvas
# Por ejemplo, aquí colocamos un botón encima de la imagen de fondo
boton = tk.Button(canvas, text="Presionar", command=mostrar_mensaje, bg="pink", fg="white", font=("times new roman", 14))
canvas.create_window(100, 100, window=boton)

# Función para cerrar la ventana
boton_cerrar = tk.Button(canvas, text="Cerrar", command=cerrar_ventana, bg="red", fg="white", font=("Arial", 12))
canvas.create_window(100, 150, window=boton_cerrar)

# Obtener las dimensiones de la imagen
ancho_imagen = imagen_fondo.width()
alto_imagen = imagen_fondo.height()

# Configurar los límites del scroll
canvas.config(scrollregion=(0, 0, ancho_imagen, alto_imagen))

# Configurar el desplazamiento del canvas con la rueda del mouse
def _on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

ventana.mainloop()
