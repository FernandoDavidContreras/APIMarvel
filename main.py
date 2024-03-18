import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import ctypes
import hashlib
import requests as req
import time
from datetime import datetime
from pprint import pprint
from list import Lista
from comic import Comic

url = f"http://gateway.marvel.com/v1/public/characters"
urlcomics = f"http://gateway.marvel.com/v1/public/comics"
urlpersonajes = f"http://gateway.marvel.com/v1/public/characters"
private_key = "d82d58686385b5490fc535829e9856c2da37fe7e"
public_key = "49034033b1faf7ef2b2535194286c4ee"
ts = time.time()

hash = hashlib.md5(f"{ts}{private_key}{public_key}".encode())


def get_comics():
    ventana_comics = tk.Toplevel()
    ventana_comics.title("Listado de Comics")
    ventana_comics.geometry("800x600")
    frame = tk.Frame(ventana_comics)
    frame.pack(fill=tk.BOTH, expand=True)
    ts = time.time()
    private_key = "d82d58686385b5490fc535829e9856c2da37fe7e"
    public_key = "49034033b1faf7ef2b2535194286c4ee"
    hash = hashlib.md5(f"{ts}{private_key}{public_key}".encode())
    urlcomics = f"http://gateway.marvel.com/v1/public/comics"

    def mostrar_comics(pagina_actual):
        global canvas
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)
        def ordenar_comics():
            nonlocal lista_comics
            opcion = variable_orden.get()
            if opcion == "Nombre":
                lista_comics.sort(key=lambda x: x.title)
            elif opcion == "Fecha de Lanzamiento":
                lista_comics.sort(key=lambda x: x.date)
            mostrar_comics(1)

            # Función para buscar cómics por nombre y año de lanzamiento
        def buscar_comics():
            nonlocal lista_comics
            nombre = entry_nombre.get().lower()
            year = entry_año.get()
            lista_filtrada = [comic for comic in lista_comics if
                              nombre in comic.title.lower() and (not year or year in comic.date)]
            lista_comics = lista_filtrada
            mostrar_comics(1)

            # Variables para la interfaz de ordenamiento y búsqueda
        variable_orden = tk.StringVar(ventana_comics)
        variable_orden.set("Nombre")
        entry_nombre = tk.Entry(ventana_comics)
        entry_año = tk.Entry(ventana_comics)
        label_orden = tk.Label(ventana_comics, text="Ordenar por:")
        label_nombre = tk.Label(ventana_comics, text="Buscar por nombre:")
        label_año = tk.Label(ventana_comics, text="Buscar por año de lanzamiento:")
        boton_ordenar = tk.Button(ventana_comics, text="Ordenar", command=ordenar_comics)
        boton_buscar = tk.Button(ventana_comics, text="Buscar", command=buscar_comics)

        label_orden.pack(padx=10, pady=10)
        tk.OptionMenu(ventana_comics, variable_orden, "Nombre", "Fecha de Lanzamiento").pack(padx=10, pady=10)
        boton_ordenar.pack(padx=10, pady=10)
        label_nombre.pack(padx=10, pady=10)
        entry_nombre.pack(padx=10, pady=10)
        label_año.pack(padx=10, pady=10)
        entry_año.pack(padx=10, pady=10)
        boton_buscar.pack(padx=10, pady=10)

        for i in range((pagina_actual - 1) * 10, min(pagina_actual * 10, len(lista_comics))):
            comic = lista_comics[i]
        response = requests.get(comic.image)
        if response.status_code == 200:
            with open("temp_image.jpg", "wb") as f:
                f.write(response.content)
            image = Image.open("temp_image.jpg")
        else:
            # Si hay un error al descargar la imagen, usa una imagen de reemplazo
            image = Image.open("imagen_de_reemplazo.jpg")

        image = image.resize((100, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(inner_frame, text=comic.title + "\n" + comic.date, image=photo, compound=tk.TOP)
        label.image = photo
        label.pack(padx=10, pady=10)
        def detalle_comic(comic=comic):
            detalle = tk.Toplevel()
            detalle.title("Detalle de Comic")
            detalle.geometry("300x300")
            label = tk.Label(detalle, text=f"Nombre: {comic.title}\nFecha de Lanzamiento: {comic.date}")
            label.pack(padx=10, pady=10)

        boton_detalle = tk.Button(inner_frame, text="Detalle", command=detalle_comic)
        boton_detalle.pack(padx=10, pady=10)


        def detalle_comic(comic=comic):
            detalle = tk.Toplevel()
            detalle.title("Detalle de Comic")
            detalle.geometry("500x500")
            tk.Label(detalle, text=f"Título: {comic.title}").pack()
            tk.Label(detalle, text=f"ISBN: {comic.isbn}").pack()
            tk.Label(detalle, text=f"Descripción: {comic.description}").pack()
        boton_detalle = tk.Button(inner_frame, text="Detalle", command=detalle_comic)
        boton_detalle.pack(padx=10, pady=10)

    params = {
        'ts': ts,
        'apikey': public_key,
        'hash': hash.hexdigest(),
        'offset': (pagina_actual - 1) * 10  # Calcular el desplazamiento para la paginación
    }
    response = req.get(urlcomics, params)
    data = response.json()['data']['results']
    lista_comics = []
    for i in data:
        id = i['id']
        title = i['title']
        image = i['thumbnail']['path'] + '.' + i['thumbnail']['extension']
        date = datetime.strptime(i['dates'][0]['date'], '%Y-%m-%dT%H:%M:%S-%f').strftime('%Y-%m')
        isbn = i['isbn']
        description = i['description']
        characters = [char['name'] for char in i['characters']['items']]
        creators = [creator['name'] for creator in i['creators']['items']]
        comic = Comic(id, title, image, date, isbn, description, characters, creators)
        lista_comics.append(comic)
    mostrar_comics(pagina_actual)
pagina_actual = 1



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
