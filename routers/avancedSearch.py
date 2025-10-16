from fastapi import APIRouter
from services.paisService import advancedSearch
from services.models import CountryFilter

router = APIRouter(prefix="/countries",tags=["Filtros"])

@router.post("/search")
async def postMetrics(countris : CountryFilter):

    return await advancedSearch(countris)
