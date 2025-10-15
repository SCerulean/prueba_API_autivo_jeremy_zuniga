import requests
from fastapi import APIRouter
from services.paisService import RuteCountryAtoB

router = APIRouter(prefix="/rute",tags=["routes"])

@router.get("/route")
async def getRute(codeA: str,codeB: str):
    return await RuteCountryAtoB(codeA,codeB)



