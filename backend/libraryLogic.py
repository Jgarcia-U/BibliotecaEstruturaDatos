from .dataStructures import libros, usuarios, historialPrestamos, listaEspera

def buscarLibro(idLibro):
    for libro in libros:
        if libro["id"] == idLibro:
            return libro
    return None

def buscarUsuario(idUsuario):
    for usuario in usuarios:
        if usuario["id"] == idUsuario:
            return usuario
    return None

def agregarLibroBackend(idLibro, titulo, autor):
    
    for libro in libros:
        if libro["id"] == idLibro:
            return "Error: Ya existe un libro con este ID."

    libro = {
        "id": idLibro,
        "titulo": titulo,
        "autor": autor,
        "disponible": True,
        "usuarioActual": None
    }
    libros.append(libro)

def agregarUsuarioBackend(idUsuario, nombre):

    for usuario in usuarios:
        if usuario["id"] == idUsuario:
            return "Error: Ya existe un usuario con este ID."

    usuario = {
        "id": idUsuario,
        "nombre": nombre,
        "librosPrestados": []
    }
    usuarios.append(usuario)

def prestarLibroBackend(idLibro, idUsuario):
    libro = buscarLibro(idLibro)
    usuario = buscarUsuario(idUsuario)

    if not libro:
        return "Libro no encontrado"
    if not usuario:
        return "Usuario no encontrado"

    if libro["disponible"]:
        libro["disponible"] = False
        libro["usuarioActual"] = idUsuario
        usuario["librosPrestados"].append(idLibro)
        historialPrestamos.append((idLibro, idUsuario))
        return "Libro prestado con éxito"
    else:
        listaEspera.append((idLibro, idUsuario))
        return "Libro no disponible. Usuario agregado a la lista de espera."

def devolverLibroBackend(idLibro):
    libro = buscarLibro(idLibro)

    if not libro:
        return "Libro no encontrado"
    if libro["disponible"]:
        return "El libro no está prestado"

    idUsuario = libro["usuarioActual"]
    usuario = buscarUsuario(idUsuario)

    libro["disponible"] = True
    libro["usuarioActual"] = None
    usuario["librosPrestados"].remove(idLibro)

    msg = " Libro devuelto con éxito"

    if listaEspera:
        siguiente = listaEspera.popleft()
        msg += f"\nPróximo usuario en espera: {siguiente[1]}"

    return msg
