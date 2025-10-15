import requests
from fastapi import APIRouter
from services.paisService import regionMetrics
router = APIRouter(prefix="/regions",tags=["regionCode"])

@router.get("/{region}/stats")
async def getMetrics(region):
    return await regionMetrics(region)

