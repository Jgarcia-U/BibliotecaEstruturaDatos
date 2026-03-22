from .data_structures import libros, usuarios, historial_prestamos, lista_espera

def buscar_libro(id_libro):
    for libro in libros:
        if libro["id"] == id_libro:
            return libro
    return None

def buscar_usuario(id_usuario):
    for usuario in usuarios:
        if usuario["id"] == id_usuario:
            return usuario
    return None

def agregar_libro_backend(id_libro, titulo, autor):
    libro = {
        "id": id_libro,
        "titulo": titulo,
        "autor": autor,
        "disponible": True,
        "usuario_actual": None
    }
    libros.append(libro)

def agregar_usuario_backend(id_usuario, nombre):
    usuario = {
        "id": id_usuario,
        "nombre": nombre,
        "libros_prestados": []
    }
    usuarios.append(usuario)

def prestar_libro_backend(id_libro, id_usuario):
    libro = buscar_libro(id_libro)
    usuario = buscar_usuario(id_usuario)

    if not libro:
        return "Libro no encontrado"
    if not usuario:
        return "Usuario no encontrado"

    if libro["disponible"]:
        libro["disponible"] = False
        libro["usuario_actual"] = id_usuario
        usuario["libros_prestados"].append(id_libro)
        historial_prestamos.append((id_libro, id_usuario))
        return "Libro prestado con éxito"
    else:
        lista_espera.append((id_libro, id_usuario))
        return "Libro no disponible. Usuario agregado a la lista de espera."

def devolver_libro_backend(id_libro):
    libro = buscar_libro(id_libro)

    if not libro:
        return "Libro no encontrado"
    if libro["disponible"]:
        return "El libro no está prestado"

    id_usuario = libro["usuario_actual"]
    usuario = buscar_usuario(id_usuario)

    libro["disponible"] = True
    libro["usuario_actual"] = None
    usuario["libros_prestados"].remove(id_libro)

    msg = " Libro devuelto con éxito"

    if lista_espera:
        siguiente = lista_espera.popleft()
        msg += f"\nPróximo usuario en espera: {siguiente[1]}"

    return msg
