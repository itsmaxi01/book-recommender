from services.auth_service import ejecutar_login
from services.book_service import importar_desde_api
from services.user_service import gestionar_usuarios
from services.recommendation_service import (
    mostrar_recomendaciones,
    alimentar_motor_usuario
)
from database.connection import conectar


if __name__ == "__main__":

    while True:

        datos_usuario = ejecutar_login()

        if datos_usuario == "EXIT":
            break

        if datos_usuario:

            id_u, nombre_u, tipo_u, primer_ingreso = datos_usuario

            print(f"\n Acceso concedido. Bienvenido, {nombre_u}!")

            if tipo_u == 1:

                while True:

                    print("\n[MODO ADMINISTRADOR]")
                    print("1. Sincronizar libros con la API")
                    print("2. Gestionar Usuarios")
                    print("3. Ver últimos 5 libros en sistema")
                    print("4. Cerrar Sesión")

                    op_admin = input("\nSelecciona una opción: ")

                    if op_admin == '1':
                        importar_desde_api()

                    elif op_admin == '2':
                        gestionar_usuarios()

                    elif op_admin == '3':

                        db = conectar()
                        cursor = db.cursor()

                        cursor.execute(
                            "SELECT titulo FROM libros ORDER BY id_libro DESC LIMIT 5"
                        )

                        for lib in cursor.fetchall():
                            print(f"• {lib[0]}")

                        db.close()

                    elif op_admin == '4':
                        break

            else:

                if primer_ingreso == 1:
                    alimentar_motor_usuario(id_u)

                else:
                    mostrar_recomendaciones(id_u)

            input("\nPresiona Enter para continuar...")

        else:
            print("\n Usuario o contraseña incorrectos.")

