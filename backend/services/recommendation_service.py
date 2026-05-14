from backend.database.connection import conectar


def alimentar_motor_usuario(id_usuario):

    db = conectar()
    cursor = db.cursor(dictionary=True)

    print("\n--- ¡VAMOS A CONFIGURAR TU PERFIL! ---")

    cursor.execute("SELECT DISTINCT genero FROM libros")

    generos = [row['genero'] for row in cursor.fetchall()]

    print("\nGéneros disponibles:")

    for i, g in enumerate(generos, 1):
        print(f"{i}. {g}")

    try:
        seleccion = int(input("\nSelecciona el número de tu género favorito: "))
        genero_elegido = generos[seleccion - 1]

    except (ValueError, IndexError):
        genero_elegido = "General"

    print(f"\nMostrando libros de {genero_elegido}:")

    cursor.execute(
        "SELECT id_libro, titulo, autor FROM libros WHERE genero = %s ORDER BY RAND() LIMIT 5",
        (genero_elegido,)
    )

    libros_a_calificar = cursor.fetchall()

    if not libros_a_calificar:
        print("No hay libros suficientes.")
        return

    for libro in libros_a_calificar:

        while True:

            try:
                calif = int(input(
                    f"¿Qué puntuación le das a '{libro['titulo']}'? (1-5): "
                ))

                if 1 <= calif <= 5:

                    cursor.execute(
                        "INSERT INTO puntuacion (id_usuario, id_libro, calificacion) VALUES (%s, %s, %s)",
                        (id_usuario, libro['id_libro'], calif)
                    )

                    break

                else:
                    print("Del 1 al 5.")

            except ValueError:
                print("Número inválido.")

    cursor.execute(
        "UPDATE usuarios SET primer_ingreso = 0 WHERE id_usuario = %s",
        (id_usuario,)
    )

    db.commit()
    db.close()

    print("\n¡Perfil configurado!")


def mostrar_recomendaciones(id_usuario):

    db = conectar()
    cursor = db.cursor(dictionary=True)

    sql_generos = """
        SELECT l.genero, AVG(p.calificacion) as promedio
        FROM puntuacion p
        JOIN libros l ON p.id_libro = l.id_libro
        WHERE p.id_usuario = %s
        GROUP BY l.genero
        ORDER BY promedio DESC, COUNT(*) DESC
        LIMIT 2
    """

    cursor.execute(sql_generos, (id_usuario,))
    mejores_generos = cursor.fetchall()

    libros_finales = []

    if mejores_generos:

        gen_1 = mejores_generos[0]['genero']

        cursor.execute("""
            SELECT id_libro, titulo, autor, genero
            FROM libros
            WHERE genero = %s
            AND id_libro NOT IN (
                SELECT id_libro
                FROM puntuacion
                WHERE id_usuario = %s
            )
            ORDER BY RAND()
            LIMIT 3
        """, (gen_1, id_usuario))

        libros_finales.extend(cursor.fetchall())

        if len(mejores_generos) > 1:

            gen_2 = mejores_generos[1]['genero']

            cursor.execute("""
                SELECT id_libro, titulo, autor, genero
                FROM libros
                WHERE genero = %s
                AND id_libro NOT IN (
                    SELECT id_libro
                    FROM puntuacion
                    WHERE id_usuario = %s
                )
                ORDER BY RAND()
                LIMIT 1
            """, (gen_2, id_usuario))

            libros_finales.extend(cursor.fetchall())

        cursor.execute("""
            SELECT id_libro, titulo, autor, genero
            FROM libros
            WHERE genero != %s
            AND id_libro NOT IN (
                SELECT id_libro
                FROM puntuacion
                WHERE id_usuario = %s
            )
            ORDER BY RAND()
            LIMIT 1
        """, (gen_1, id_usuario))

        libros_finales.extend(cursor.fetchall())

    if len(libros_finales) < 5:

        faltantes = 5 - len(libros_finales)

        ids_ya_incluidos = [l['id_libro'] for l in libros_finales]

        if not ids_ya_incluidos:
            ids_ya_incluidos = [0]

        ids_str = ",".join(map(str, ids_ya_incluidos))

        query_fill = f"""
            SELECT id_libro, titulo, autor, genero
            FROM libros
            WHERE id_libro NOT IN ({ids_str})
            AND id_libro NOT IN (
                SELECT id_libro
                FROM puntuacion
                WHERE id_usuario = %s
            )
            ORDER BY RAND()
            LIMIT {faltantes}
        """

        cursor.execute(query_fill, (id_usuario,))
        libros_finales.extend(cursor.fetchall())

    print("\n" + "=" * 50)
    print("   TUS RECOMENDACIONES PERSONALIZADAS ")
    print("=" * 50)

    if not libros_finales:
        print(" ¡Vaya! No encontramos libros nuevos para recomendarte.")

    else:

        for i, l in enumerate(libros_finales, 1):

            if mejores_generos and i <= 3 and l['genero'] == mejores_generos[0]['genero']:
                tag = " [Recomendado]"
            elif i == 5:
                tag = " [Nuevo]"
            else:
                tag = " [Podría gustarte]"

            print(f"{i}. {tag} {l['titulo']} - {l['autor']} | {l['genero']} (ID: {l['id_libro']})")

    print("\n" + "-" * 50)

    opcion = input("¿Quieres calificar alguno de estos libros ahora? (s/n): ")

    if opcion.lower() == 's':

        try:
            num = int(input("Ingresa el número de la lista (1-5): "))

            if 1 <= num <= len(libros_finales):

                libro_sel = libros_finales[num - 1]

                calif = int(input(
                    f"¿Qué calificación le das a '{libro_sel['titulo']}'? (1-5): "
                ))

                if 1 <= calif <= 5:

                    sql_ins = """
                        INSERT INTO puntuacion
                        (id_usuario, id_libro, calificacion)
                        VALUES (%s, %s, %s)
                    """

                    cursor.execute(
                        sql_ins,
                        (id_usuario, libro_sel['id_libro'], calif)
                    )

                    db.commit()

                    print(
                        f"¡Guardado! Tu opinión sobre '{libro_sel['titulo']}' nos ayuda a mejorar."
                    )

                else:
                    print("Debe ser entre 1 y 5.")

            else:
                print("Selección fuera de rango.")

        except ValueError:
            print("Por favor, usa números.")

    db.close()