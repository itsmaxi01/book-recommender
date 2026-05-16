from fastapi import APIRouter
from services.book_service import obtener_libros

router = APIRouter()

@router.get("/books")
def get_books():

    return obtener_libros()