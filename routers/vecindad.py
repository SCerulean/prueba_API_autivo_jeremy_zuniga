import requests
from fastapi import APIRouter
from services.paisService import  neighbors

router = APIRouter(prefix="/vecindad",tags=["Code"])


@router.get("/{code}/neighbors")
async def get_pais(code: str):
    return await neighbors(code)

