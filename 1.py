import tkinter as tk
from tkinter import ttk

class Comic:
    def __init__(self, nombre, imagen, fecha_lanzamiento):
        self.nombre = nombre
        self.imagen = imagen
        self.fecha_lanzamiento = fecha_lanzamiento

class Personaje:
    def __init__(self, nombre, imagen):
        self.nombre = nombre
        self.imagen = imagen

class TiendaMarvelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tienda de Cómics Marvel")

        self.tabControl = ttk.Notebook(self.root)

        self.comics_frame = ttk.Frame(self.tabControl)
        self.personajes_frame = ttk.Frame(self.tabControl)

        self.tabControl.add(self.comics_frame, text="Comics")
        self.tabControl.add(self.personajes_frame, text="Personajes")
        self.tabControl.pack(expand=1, fill="both")

        self.initialize_comics_tab()
        self.initialize_personajes_tab()

    def initialize_comics_tab(self):
        self.comics_listbox = tk.Listbox(self.comics_frame)
        self.comics_listbox.pack(fill="both", expand=True)

        self.search_entry = ttk.Entry(self.comics_frame)
        self.search_entry.pack(pady=5)

        search_button = ttk.Button(self.comics_frame, text="Buscar", command=self.search_comics)
        search_button.pack()

    def initialize_personajes_tab(self):
        self.personajes_listbox = tk.Listbox(self.personajes_frame)
        self.personajes_listbox.pack(fill="both", expand=True)

        self.search_entry_personajes = ttk.Entry(self.personajes_frame)
        self.search_entry_personajes.pack(pady=5)

        search_button_personajes = ttk.Button(self.personajes_frame, text="Buscar", command=self.search_personajes)
        search_button_personajes.pack()

    def search_comics(self):
        query = self.search_entry.get()
        # Lógica de búsqueda de cómics
        pass

    def search_personajes(self):
        query = self.search_entry_personajes.get()
        # Lógica de búsqueda de personajes
        pass

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaMarvelApp(root)
    root.mainloop()
