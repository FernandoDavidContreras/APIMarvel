import tkinter as tk
from tkinter import ttk, messagebox
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
    ventana_comics.geometry("800x400")

    response = req.get("http://gateway.marvel.com/v1/public/comics", params={
        "apikey": public_key,
        "ts": ts,
        "hash": hash.hexdigest(),
        "limit": 50
    })

    data = response.json()

    if "data" in data and "results" in data["data"]:
        canvas = tk.Canvas(ventana_comics)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(ventana_comics, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar = ttk.Scrollbar(ventana_comics, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.configure(xscrollcommand=scrollbar.set)

        frame_comics = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_comics, anchor=tk.NW)

        row = 0
        col = 0
        for i, comic_data in enumerate(data["data"]["results"]):
            title = comic_data["title"]
            isbn = comic_data.get("isbn", "No disponible")
            descripcion = comic_data.get("description", "No disponible")
            image_url = comic_data["thumbnail"]["path"] + "." + comic_data["thumbnail"]["extension"]

            frame_comic = tk.Frame(frame_comics)
            frame_comic.grid(row=row, column=col, padx=10, pady=10)

            tk.Label(frame_comic, text=title, font=("Arial", 12, "bold")).pack(side=tk.TOP)

            response = requests.get(image_url)
            if response.status_code == 200:
                with open(f"temp_image_{title}.jpg", "wb") as f:
                    f.write(response.content)
                image = Image.open(f"temp_image_{title}.jpg")
            else:
                image = Image.open("imagen_de_reemplazo.jpg")

            image = image.resize((100, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            label_imagen = tk.Label(frame_comic, image=photo)
            label_imagen.image = photo
            label_imagen.pack(side=tk.TOP, padx=10, pady=5)

            def ver_detalles(titulo=title, isbn=isbn, descripcion=descripcion):
                detalle_ventana = tk.Toplevel()
                detalle_ventana.title("Detalles del Comic")
                detalle_ventana.geometry("400x300")
                tk.Label(detalle_ventana, text=f"Título: {titulo}", font=("Arial", 12, "bold")).pack(side=tk.TOP)
                tk.Label(detalle_ventana, text=f"ISBN: {isbn}", font=("Arial", 12, "bold")).pack(side=tk.TOP)
                tk.Label(detalle_ventana, text=f"Descripción del Comic:", font=("Arial", 12, "bold")).pack(
                    side=tk.TOP)
                tk.Label(detalle_ventana, text=descripcion, wraplength=380).pack(side=tk.TOP, padx=10, pady=5)

            boton_detalle = tk.Button(frame_comic, text="Ver detalles", command=ver_detalles)
            boton_detalle.pack(side=tk.TOP, padx=10, pady=5)

            if col == 9:  # Si se alcanza el límite de 10 elementos por fila, pasa a la siguiente fila
                col = 0
                row += 1
            else:
                col += 1

        # Ajustar el tamaño del canvas
        frame_comics.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    boton_salir = tk.Button(ventana_comics, text="Salir", command=ventana_comics.destroy,
                            font=("times new roman", 18), bg="Red", fg="black",
                            width=18, height=2, bd=12)
    boton_salir.pack(pady=5)


def buscar_comic_por_nombre(nombre):
    response = req.get(urlcomics, params={
        "apikey": public_key,
        "ts": ts,
        "hash": hash.hexdigest(),
        "titleStartsWith": nombre
    })

    data = response.json()

    if "data" in data and "results" in data["data"]:
        return data["data"]["results"]
    else:
        return None


def buscar_comic_por_fecha(fecha):
    year = fecha.split("-")[0]
    response = req.get(urlcomics, params={
        "apikey": public_key,
        "ts": ts,
        "hash": hash.hexdigest(),
        "dateRange": f"{year}-01-01,{year}-12-31"
    })

    data = response.json()

    if "data" in data and "results" in data["data"]:
        return data["data"]["results"]
    else:
        return None


def buscar_comic():
    ventana_buscar = tk.Toplevel()
    ventana_buscar.title("Buscar Comic")
    ventana_buscar.geometry("400x200")

    def buscar():
        tipo_busqueda = seleccion.get()
        valor_busqueda = entry_busqueda.get()

        if tipo_busqueda == "Nombre":
            resultados = buscar_comic_por_nombre(valor_busqueda)
        else:
            resultados = buscar_comic_por_fecha(valor_busqueda)

        if resultados:
            mostrar_resultados(resultados)
        else:
            tk.messagebox.showinfo("Comic no encontrado", "El comic no existe.")

    seleccion = ttk.Combobox(ventana_buscar, values=["Nombre", "Fecha"])
    seleccion.set("Nombre")
    seleccion.pack(pady=10)

    entry_busqueda = tk.Entry(ventana_buscar)
    entry_busqueda.pack(pady=5)

    boton_buscar = tk.Button(ventana_buscar, text="Buscar", command=buscar)
    boton_buscar.pack(pady=5)


def mostrar_resultados(resultados):
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de la búsqueda")
    ventana_resultados.geometry("800x400")

    canvas = tk.Canvas(ventana_resultados)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(ventana_resultados, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar = ttk.Scrollbar(ventana_resultados, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(xscrollcommand=scrollbar.set)

    frame_resultados = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_resultados, anchor=tk.NW)

    row = 0
    col = 0
    for i, comic_data in enumerate(resultados):
        title = comic_data["title"]
        isbn = comic_data.get("isbn", "No disponible")
        descripcion = comic_data.get("description", "No disponible")
        image_url = comic_data["thumbnail"]["path"] + "." + comic_data["thumbnail"]["extension"]

        frame_comic = tk.Frame(frame_resultados)
        frame_comic.grid(row=row, column=col, padx=10, pady=10)

        tk.Label(frame_comic, text=title, font=("Arial", 12, "bold")).pack(side=tk.TOP)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f"temp_image_{title}.jpg", "wb") as f:
                f.write(response.content)
            image = Image.open(f"temp_image_{title}.jpg")
        else:
            image = Image.open("imagen_de_reemplazo.jpg")

        image = image.resize((100, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label_imagen = tk.Label(frame_comic, image=photo)
        label_imagen.image = photo
        label_imagen.pack(side=tk.TOP, padx=10, pady=5)

        def ver_detalles(titulo=title, isbn=isbn, descripcion=descripcion):
            detalle_ventana = tk.Toplevel()
            detalle_ventana.title("Detalles del Comic")
            detalle_ventana.geometry("400x300")
            tk.Label(detalle_ventana, text=f"Título: {titulo}", font=("Arial", 12, "bold")).pack(side=tk.TOP)
            tk.Label(detalle_ventana, text=f"ISBN: {isbn}", font=("Arial", 12, "bold")).pack(side=tk.TOP)
            tk.Label(detalle_ventana, text=f"Descripción del Comic:", font=("Arial", 12, "bold")).pack(
                side=tk.TOP)
            tk.Label(detalle_ventana, text=descripcion, wraplength=380).pack(side=tk.TOP, padx=10, pady=5)

        boton_detalle = tk.Button(frame_comic, text="Ver detalles", command=ver_detalles)
        boton_detalle.pack(side=tk.TOP, padx=10, pady=5)

        if col == 9:  # Si se alcanza el límite de 10 elementos por fila, pasa a la siguiente fila
            col = 0
            row += 1
        else:
            col += 1

    # Ajustar el tamaño del canvas
    frame_resultados.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def comic_detalle():
    buscar_comic()


def comic_area():
    ventana3 = tk.Toplevel(ventana)
    ventana3.title("Área de comics")
    ventana3.geometry("700x700")
    etiqueta_menu = tk.Label(ventana3, text="¿ Qué desea hacer ?", font=("times new roman", 14))
    etiqueta_menu.pack(pady=20)
    botonc = tk.Button(ventana3, text=" Listado de comics ", command=get_comics, font=("Comic Sans MS", 18), bg="Azure",
                       fg="black", width=18, height=2, bd=12)
    botonc.pack(pady=5)
    botonl = tk.Button(ventana3, text=" Detalles de un comic ", command=comic_detalle, font=("Comic Sans MS", 18),
                       bg="Azure",
                       fg="black", width=18, height=2, bd=12)
    botonl.pack(pady=5)

    def salir():
        ventana3.destroy()

    boton1 = tk.Button(ventana3, text="Salir", command=salir, font=("times new roman", 18), bg="Red", fg="black",
                       width=18, height=2, bd=12)
    boton1.pack(pady=5)


def get_personaje():
    ventana_personajes = tk.Toplevel()
    ventana_personajes.title("Listado de Personajes")
    ventana_personajes.geometry("800x400")

    response = req.get("http://gateway.marvel.com/v1/public/characters", params={
        "apikey": public_key,
        "ts": ts,
        "hash": hash.hexdigest(),
        "limit": 50
    })

    data = response.json()

    if "data" in data and "results" in data["data"]:
        canvas = tk.Canvas(ventana_personajes)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(ventana_personajes, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar = ttk.Scrollbar(ventana_personajes, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.configure(xscrollcommand=scrollbar.set)

        frame_personajes = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_personajes, anchor=tk.NW)

        row = 0
        col = 0
        for i, personaje_data in enumerate(data["data"]["results"]):
            nombre = personaje_data["name"]
            descripcion = personaje_data.get("description", "No disponible")
            imagen_url = personaje_data["thumbnail"]["path"] + "." + personaje_data["thumbnail"]["extension"]

            frame_personaje = tk.Frame(frame_personajes)
            frame_personaje.grid(row=row, column=col, padx=10, pady=10)

            tk.Label(frame_personaje, text=nombre, font=("Arial", 12, "bold")).pack(side=tk.TOP)

            response = requests.get(imagen_url)
            if response.status_code == 200:
                with open(f"temp_image_{nombre}.jpg", "wb") as f:
                    f.write(response.content)
                image = Image.open(f"temp_image_{nombre}.jpg")
            else:
                image = Image.open("imagen_de_reemplazo.jpg")

            image = image.resize((100, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            label_imagen = tk.Label(frame_personaje, image=photo)
            label_imagen.image = photo
            label_imagen.pack(side=tk.TOP, padx=10, pady=5)

            def ver_detalles(descripcion=descripcion):
                detalle_ventana = tk.Toplevel()
                detalle_ventana.title("Detalles del Personaje")
                detalle_ventana.geometry("400x300")
                tk.Label(detalle_ventana, text="Descripción del Personaje:", font=("Arial", 12, "bold")).pack(
                    side=tk.TOP)
                tk.Label(detalle_ventana, text=descripcion, wraplength=380).pack(side=tk.TOP, padx=10, pady=5)

            boton_detalle = tk.Button(frame_personaje, text="Ver detalles", command=ver_detalles)
            boton_detalle.pack(side=tk.TOP, padx=10, pady=5)

            if col == 9:  # Si se alcanza el límite de 10 elementos por fila, pasa a la siguiente fila
                col = 0
                row += 1
            else:
                col += 1

        # Ajustar el tamaño del canvas
        frame_personajes.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    boton_salir = tk.Button(ventana_personajes, text="Salir", command=ventana_personajes.destroy,
                            font=("times new roman", 18), bg="Red", fg="black",
                            width=18, height=2, bd=12)
    boton_salir.pack(pady=5)


def buscar_personaje_por_nombre(nombre):
    response = req.get("http://gateway.marvel.com/v1/public/characters", params={
        "apikey": public_key,
        "ts": ts,
        "hash": hash.hexdigest(),
        "nameStartsWith": nombre
    })

    data = response.json()

    if "data" in data and "results" in data["data"]:
        return data["data"]["results"]
    else:
        return None


def buscar_personaje():
    ventana_buscar = tk.Toplevel()
    ventana_buscar.title("Buscar Personaje")
    ventana_buscar.geometry("400x200")

    def buscar():
        valor_busqueda = entry_busqueda.get()

        resultados = buscar_personaje_por_nombre(valor_busqueda)

        if resultados:
            mostrar_resultados_personajes(resultados)
        else:
            tk.messagebox.showinfo("Personaje no encontrado", "El personaje no existe.")

    entry_busqueda = tk.Entry(ventana_buscar)
    entry_busqueda.pack(pady=10)

    boton_buscar = tk.Button(ventana_buscar, text="Buscar", command=buscar)
    boton_buscar.pack(pady=5)


def mostrar_resultados_personajes(resultados):
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de la búsqueda")
    ventana_resultados.geometry("800x400")

    canvas = tk.Canvas(ventana_resultados)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(ventana_resultados, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar = ttk.Scrollbar(ventana_resultados, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(xscrollcommand=scrollbar.set)


    frame_resultados = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_resultados, anchor=tk.NW)

    row = 0
    col = 0
    for i, personaje_data in enumerate(resultados):
        nombre = personaje_data["name"]
        descripcion = personaje_data.get("description", "No disponible")
        image_url = personaje_data["thumbnail"]["path"] + "." + personaje_data["thumbnail"]["extension"]

        frame_personaje = tk.Frame(frame_resultados)
        frame_personaje.grid(row=row, column=col, padx=10, pady=10)

        tk.Label(frame_personaje, text=nombre, font=("Arial", 12, "bold")).pack(side=tk.TOP)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f"temp_image_{nombre}.jpg", "wb") as f:
                f.write(response.content)
            image = Image.open(f"temp_image_{nombre}.jpg")
        else:
            image = Image.open("imagen_de_reemplazo.jpg")

        image = image.resize((100, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label_imagen = tk.Label(frame_personaje, image=photo)
        label_imagen.image = photo
        label_imagen.pack(side=tk.TOP, padx=10, pady=5)

        def ver_detalles(descripcion=descripcion):
            detalle_ventana = tk.Toplevel()
            detalle_ventana.title("Detalles del Personaje")
            detalle_ventana.geometry("400x300")
            tk.Label(detalle_ventana, text="Descripción del Personaje:", font=("Arial", 12, "bold")).pack(
                side=tk.TOP)
            tk.Label(detalle_ventana, text=descripcion, wraplength=380).pack(side=tk.TOP, padx=10, pady=5)

        boton_detalle = tk.Button(frame_personaje, text="Ver detalles", command=ver_detalles)
        boton_detalle.pack(side=tk.TOP, padx=10, pady=5)

        if col == 9:  # Si se alcanza el límite de 10 elementos por fila, pasa a la siguiente fila
            col = 0
            row += 1
        else:
            col += 1

    # Ajustar el tamaño del canvas
    frame_resultados.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def personaje_detalle():
    buscar_personaje()


def personaje_area():
    ventana4 = tk.Toplevel(ventana)
    ventana4.geometry("700x700")
    ventana4.title("Área de personaje")
    etiqueta_menu = tk.Label(ventana4, text="¿ Qué desea hacer ?", font=("times new roman", 14))
    etiqueta_menu.pack(pady=20)
    botonc = tk.Button(ventana4, text=" Listado de personajes ", command=get_personaje, font=("Comic Sans MS", 18),
                       bg="Azure",
                       fg="black", width=18, height=2, bd=12)
    botonc.pack(pady=5)
    botonl = tk.Button(ventana4, text=" Detalles de un personaje ", command=personaje_detalle,
                       font=("Comic Sans MS", 18), bg="Azure",
                       fg="black", width=18, height=2, bd=12)
    botonl.pack(pady=5)

    def salir():
        ventana4.destroy()

    boton1 = tk.Button(ventana4, text="Salir", command=salir, font=("times new roman", 18), bg="Red", fg="black",
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
    boton1 = tk.Button(ventana2, text="Ver área de personajes", command=personaje_area, font=("Comic Sans MS", 18),
                       bg="Cyan",
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
