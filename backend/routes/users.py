from fastapi import APIRouter
from pydantic import BaseModel

from services.recommendation_service import (
    finalizar_primer_ingreso
)

router = APIRouter()


class UserData(BaseModel):

    id_usuario: int


@router.put("/finish-onboarding")
def finish_onboarding(datos: UserData):

    resultado = finalizar_primer_ingreso(
        datos.id_usuario
    )

    return resultado