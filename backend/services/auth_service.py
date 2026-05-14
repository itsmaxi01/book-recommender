from backend.database.connection import conectar


def ejecutar_login():

    db = conectar()
    cursor = db.cursor()

    print("\n" + "=" * 30 + "\n   SISTEMA DE LIBROS    \n" + "=" * 30)

    user = input("Usuario (o 'exit'): ")

    if user.lower() == 'exit':
        return "EXIT"

    psw = input("Contraseña: ")

    sql = """
        SELECT id_usuario, username, tipo, primer_ingreso
        FROM usuarios
        WHERE username = %s
        AND contrasena = %s
    """

    cursor.execute(sql, (user, psw))

    resultado = cursor.fetchone()

    db.close()

    return resultado
