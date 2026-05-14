from backend.database.connection import conectar
import requests
import random

def importar_desde_api():
    temas = ["fiction", "horror", "sci-fi", "history", "fantasy", "mystery", "thriller", "science", "biography"]
    tema_azar = random.choice(temas)
    pagina_azar = random.randint(1, 100)

    print(f"\n [API] Trayendo libros de '{tema_azar}' (Página {pagina_azar})...")
    url = f"https://openlibrary.org/search.json?q={tema_azar}&limit=10&page={pagina_azar}"

    try:
        res = requests.get(url).json()
        db = conectar()
        cursor = db.cursor()

        libros_nuevos = 0

        for doc in res.get('docs', []):
            titulo = doc.get('title', 'Sin título')[:100]
            autor = doc.get('author_name', ['Anónimo'])[0][:50]
            anio = doc.get('first_publish_year', 0)

            generos_api = doc.get('subject', [])
            genero = "General"

            for g in generos_api:
                if g.lower() not in ["fiction", "general", "accessible book", "protected daisy"]:
                    genero = g.capitalize()
                    break

            if genero == "General":
                genero = tema_azar.capitalize()

            query = """
                INSERT IGNORE INTO libros
                (titulo, genero, autor, anio)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (titulo, genero, autor, anio))

            if cursor.rowcount > 0:
                libros_nuevos += 1

        db.commit()
        db.close()

        print(f" ¡Éxito! Se agregaron {libros_nuevos} libros nuevos.")

    except Exception as e:
        print(f" Error en la API: {e}")
