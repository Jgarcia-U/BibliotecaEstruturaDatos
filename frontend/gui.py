import tkinter as tk
from tkinter import messagebox

from backend.libraryLogic import (
    agregarLibroBackend,
    agregarUsuarioBackend,
    prestarLibroBackend,
    devolverLibroBackend,
    historialPrestamos
)

class BibliotecaGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("400x400")

        tk.Label(root, text="SISTEMA DE BIBLIOTECA", font=("Arial", 16)).pack(pady=10)

        tk.Button(root, text="Agregar Libro", width=25, command=self.ventanaAgregarLibro).pack(pady=5)
        tk.Button(root, text="Agregar Usuario", width=25, command=self.ventanaAgregarUsuario).pack(pady=5)
        tk.Button(root, text="Prestar Libro", width=25, command=self.ventanaPrestarLibro).pack(pady=5)
        tk.Button(root, text="Devolver Libro", width=25, command=self.ventanaDevolverLibro).pack(pady=5)
        tk.Button(root, text="Ver historial", width=25, command=self.verHistorial).pack(pady=5)
        tk.Button(root, text="Ver libros", width=25, command=self.verLibros).pack(pady=5)

    # Ventanas de formularios
    def ventanaAgregarLibro(self):
        win = tk.Toplevel()
        win.title("Agregar Libro")

        tk.Label(win, text="ID del libro").pack()
        idLibro = tk.Entry(win)
        idLibro.pack()

        tk.Label(win, text="Título").pack()
        titulo = tk.Entry(win)
        titulo.pack()

        tk.Label(win, text="Autor").pack()
        autor = tk.Entry(win)
        autor.pack()

        def guardar():
            msg = agregarLibroBackend(idLibro.get(), titulo.get(), autor.get())

            if msg is None:
                messagebox.showinfo("Éxito", "Libro agregado correctamente.")
                win.destroy()
            else:
                messagebox.showerror("Error", msg)
        
        tk.Button(win, text="Guardar", command=guardar).pack()

    def ventanaAgregarUsuario(self):
        win = tk.Toplevel()
        win.title("Agregar Usuario")

        tk.Label(win, text="ID del usuario").pack()
        idUsuario = tk.Entry(win)
        idUsuario.pack()

        tk.Label(win, text="Nombre").pack()
        nombre = tk.Entry(win)
        nombre.pack()

        def guardar():
            msg = agregarUsuarioBackend(idUsuario.get(), nombre.get())

            if msg is None:
                messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(win, text="Guardar", command=guardar).pack()

    def ventanaPrestarLibro(self):
        win = tk.Toplevel()
        win.title("Prestar Libro")

        tk.Label(win, text="ID del libro").pack()
        idLibro = tk.Entry(win)
        idLibro.pack()

        tk.Label(win, text="ID del usuario").pack()
        idUsuario = tk.Entry(win)
        idUsuario.pack()

        def prestar():
            msg = prestarLibroBackend(idLibro.get(), idUsuario.get())
            messagebox.showinfo("Resultado", msg)
            win.destroy()

        tk.Button(win, text="Prestar", command=prestar).pack()

    def ventanaDevolverLibro(self):
        win = tk.Toplevel()
        win.title("Devolver Libro")

        tk.Label(win, text="ID del libro").pack()
        idLibro = tk.Entry(win)
        idLibro.pack()

        def devolver():
            msg = devolverLibroBackend(idLibro.get())
            messagebox.showinfo("Resultado", msg)
            win.destroy()

        tk.Button(win, text="Devolver", command=devolver).pack()

    def verHistorial(self):
        messagebox.showinfo("Historial", str(historialPrestamos))

    def verLibros(self):
        from backend.dataStructures import libros, listaEspera

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

        for libro in libros:
            estado = "Disponible" if libro["disponible"] else f"Prestado a {libro['usuarioActual']}"

            tk.Label(content, text=f"ID: {libro['id']}").pack(anchor="w")
            tk.Label(content, text=f"Título: {libro['titulo']}").pack(anchor="w")
            tk.Label(content, text=f"Autor: {libro['autor']}").pack(anchor="w")
            tk.Label(content, text=f"Estado: {estado}", 
                    fg="green" if libro["disponible"] else "red").pack(anchor="w")

            esperaLibro = [u for (idL, u) in listaEspera if idL == libro["id"]]

            if esperaLibro:
                tk.Label(content, text=f"Usuarios en espera ({len(esperaLibro)}):", fg="blue").pack(anchor="w")
                for usuario in esperaLibro:
                    tk.Label(content, text=f" - {usuario}").pack(anchor="w")
            else:
                tk.Label(content, text="Usuarios en espera: Ninguno", fg="gray").pack(anchor="w")

            tk.Label(content, text="-"*40).pack(anchor="w", pady=5)
