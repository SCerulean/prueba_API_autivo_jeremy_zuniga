from pydantic import BaseModel

class CountryFilter(BaseModel):
    minPopulation: int | None = None
    maxPopulation: int | None = None
    languages: list[str] | None = None
    region: str | None = None   
