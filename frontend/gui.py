import tkinter as tk
from tkinter import messagebox

from backend.library_logic import (
    agregar_libro_backend,
    agregar_usuario_backend,
    prestar_libro_backend,
    devolver_libro_backend,
    historial_prestamos
)

class BibliotecaGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("400x400")

        tk.Label(root, text="SISTEMA DE BIBLIOTECA", font=("Arial", 16)).pack(pady=10)

        tk.Button(root, text="Agregar Libro", width=25, command=self.ventana_agregar_libro).pack(pady=5)
        tk.Button(root, text="Agregar Usuario", width=25, command=self.ventana_agregar_usuario).pack(pady=5)
        tk.Button(root, text="Prestar Libro", width=25, command=self.ventana_prestar_libro).pack(pady=5)
        tk.Button(root, text="Devolver Libro", width=25, command=self.ventana_devolver_libro).pack(pady=5)
        tk.Button(root, text="Ver historial", width=25, command=self.ver_historial).pack(pady=5)
        tk.Button(root, text="Ver libros", width=25, command=self.ver_libros).pack(pady=5)

    # Ventanas de formularios
    def ventana_agregar_libro(self):
        win = tk.Toplevel()
        win.title("Agregar Libro")

        tk.Label(win, text="ID del libro").pack()
        id_libro = tk.Entry(win)
        id_libro.pack()

        tk.Label(win, text="Título").pack()
        titulo = tk.Entry(win)
        titulo.pack()

        tk.Label(win, text="Autor").pack()
        autor = tk.Entry(win)
        autor.pack()

        def guardar():
            agregar_libro_backend(id_libro.get(), titulo.get(), autor.get())
            messagebox.showinfo("Éxito", "Libro agregado")
            win.destroy()

        tk.Button(win, text="Guardar", command=guardar).pack()

    def ventana_agregar_usuario(self):
        win = tk.Toplevel()
        win.title("Agregar Usuario")

        tk.Label(win, text="ID del usuario").pack()
        id_usuario = tk.Entry(win)
        id_usuario.pack()

        tk.Label(win, text="Nombre").pack()
        nombre = tk.Entry(win)
        nombre.pack()

        def guardar():
            agregar_usuario_backend(id_usuario.get(), nombre.get())
            messagebox.showinfo("Éxito", "Usuario agregado")
            win.destroy()

        tk.Button(win, text="Guardar", command=guardar).pack()

    def ventana_prestar_libro(self):
        win = tk.Toplevel()
        win.title("Prestar Libro")

        tk.Label(win, text="ID del libro").pack()
        id_libro = tk.Entry(win)
        id_libro.pack()

        tk.Label(win, text="ID del usuario").pack()
        id_usuario = tk.Entry(win)
        id_usuario.pack()

        def prestar():
            msg = prestar_libro_backend(id_libro.get(), id_usuario.get())
            messagebox.showinfo("Resultado", msg)
            win.destroy()

        tk.Button(win, text="Prestar", command=prestar).pack()

    def ventana_devolver_libro(self):
        win = tk.Toplevel()
        win.title("Devolver Libro")

        tk.Label(win, text="ID del libro").pack()
        id_libro = tk.Entry(win)
        id_libro.pack()

        def devolver():
            msg = devolver_libro_backend(id_libro.get())
            messagebox.showinfo("Resultado", msg)
            win.destroy()

        tk.Button(win, text="Devolver", command=devolver).pack()

    def ver_historial(self):
        messagebox.showinfo("Historial", str(historial_prestamos))

    def ver_libros(self):
        from backend.data_structures import libros

        if not libros:
            messagebox.showinfo("Libros", "No hay libros registrados.")
            return

        win = tk.Toplevel()
        win.title("Lista de Libros")

        tk.Label(win, text="LIBROS REGISTRADOS", font=("Arial", 14)).pack(pady=10)

        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        content = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content, anchor="nw")

        # Mostrar libros
        for libro in libros:
            estado = "Disponible" if libro["disponible"] else f"Prestado a {libro['usuario_actual']}"

            tk.Label(content, text=f"ID: {libro['id']}").pack(anchor="w")
            tk.Label(content, text=f"Título: {libro['titulo']}").pack(anchor="w")
            tk.Label(content, text=f"Autor: {libro['autor']}").pack(anchor="w")
            tk.Label(content, text=f"Estado: {estado}", fg="green" if libro["disponible"] else "red").pack(anchor="w")
            tk.Label(content, text="-"*40).pack(anchor="w")
