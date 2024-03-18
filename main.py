import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import ctypes
import hashlib
import requests as req
import time
from datetime import datetime
from comic import Comic
from list import Lista

urlcomics = f"http://gateway.marvel.com/v1/public/comics"
private_key = "d82d58686385b5490fc535829e9856c2da37fe7e"
public_key = "49034033b1faf7ef2b2535194286c4ee"
ts = time.time()

hash = hashlib.md5(f"{ts}{private_key}{public_key}".encode())
lista_comics = Lista()

def get_comics():
    ventana_comics = tk.Toplevel()
    ventana_comics.title("Listado de Comics")
    ventana_comics.geometry("800x600")

    response = req.get(urlcomics, params={
        "apikey": public_key,
        "ts": ts,
        "hash": hash.hexdigest(),
        "limit": 10  # Definir el número de cómics que deseas mostrar
    })

    data = response.json()

    if "data" in data and "results" in data["data"]:
        for comic_data in data["data"]["results"]:
            title = comic_data["title"]
            isbn = comic_data.get("isbn", "No disponible")
            description = comic_data.get("description", "No disponible")
            image_url = comic_data["thumbnail"]["path"] + "." + comic_data["thumbnail"]["extension"]

            comic = Comic(title, isbn, description, image_url)
            lista_comics.append(comic)

    canvas = tk.Canvas(ventana_comics)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(ventana_comics, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

    for i in range(lista_comics.size):
        comic = lista_comics[i]

        response = requests.get(comic.image)
        if response.status_code == 200:
            with open(f"temp_image_{i}.jpg", "wb") as f:
                f.write(response.content)
            image = Image.open(f"temp_image_{i}.jpg")
        else:
            image = Image.open("imagen_de_reemplazo.jpg")

        image = image.resize((100, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(inner_frame, text=comic.title, image=photo, compound=tk.TOP)
        label.image = photo
        label.grid(row=0, column=i, padx=10, pady=10)

        def detalle_comic(comic=comic):
            detalle = tk.Toplevel()
            detalle.title("Detalle de Comic")
            detalle.geometry("500x500")
            tk.Label(detalle, text=f"Título: {comic.title}").pack()
            tk.Label(detalle, text=f"ISBN: {comic.isbn}", wraplength=400).pack()
            tk.Label(detalle, text=f"Descripción: {comic.description}", wraplength=400).pack()

        boton_detalle = tk.Button(inner_frame, text="Detalle", command=detalle_comic)
        boton_detalle.grid(row=1, column=i, padx=10, pady=10)



def comic_area():
    ventana3 = tk.Toplevel(ventana)
    ventana3.title("Área de comics")
    ventana3.geometry("700x700")
    etiqueta_menu = tk.Label(ventana3, text="¿ Qué desea hacer ?", font=("times new roman", 14))
    etiqueta_menu.pack(pady=20)
    botonc = tk.Button(ventana3, text=" Listado de comics ", command=get_comics, font=("Comic Sans MS", 18), bg="Azure",
                       fg="black", width=18, height=2, bd=12)
    botonc.pack(pady=5)
    botonl = tk.Button(ventana3, text=" Detalles de un comics ", font=("Comic Sans MS", 18), bg="Azure",
                       fg="black", width=18, height=2, bd=12)
    botonl.pack(pady=5)

    def salir():
        ventana3.destroy()

    boton1 = tk.Button(ventana3, text="Salir", command=salir, font=("times new roman", 18), bg="Red", fg="black",
                       width=18, height=2, bd=12)
    boton1.pack(pady=5)


def vermenu():
    ventana2 = tk.Toplevel(ventana)
    ventana2.title("Menú")
    ventana2.geometry("700x700")
    etiqueta_menu = tk.Label(ventana2, text="¿ Qué desea hacer ?", font=("times new roman", 14))
    etiqueta_menu.pack(pady=20)
    boton0 = tk.Button(ventana2, text="Ver área de comics", command=comic_area, font=("Comic Sans MS", 18), bg="Navy",
                       fg="white", width=18, height=2, bd=12)
    boton0.pack(pady=5)
    boton1 = tk.Button(ventana2, text="Ver área de personajes", command=vermenu, font=("Comic Sans MS", 18), bg="Cyan",
                       fg="black", width=18, height=2, bd=12)
    boton1.pack(pady=5)

    def salir():
        ventana2.destroy()

    boton1 = tk.Button(ventana2, text="Salir", command=salir, font=("times new roman", 18), bg="Red", fg="black",
                       width=18, height=2, bd=12)
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
tamano_boton_x = 300
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
