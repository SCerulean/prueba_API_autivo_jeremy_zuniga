import httpx


BASE_URL = "https://restcountries.com/v3.1"

URL_COUNTRYS = "https://restcountries.com/v3.1/alpha"



async def searchCountry(code):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{URL_COUNTRYS}/{code}?fields=name,borders,population,capital,languages")

        if response.status_code != 200:
            return {"error" : f" no se encontro el pais '{code}'"}
        data = response.json()
        return data
    




async def neighbors(code):
    mainCountry = await searchCountry(code)

    if not mainCountry:
        return None
    
    bordersCountrys = []

    #separar la data del pais buscado
    country = mainCountry["name"]["common"]
    countryLanguages = set(mainCountry.get("languages",{}).values())
    countryPopulation = mainCountry.get("population")
    countryCapital = mainCountry.get("capital")
    borderscountry = mainCountry.get("borders",[])


    print(countryPopulation)

    #comparar lenguajes 
    comparacion = {}
    capitales = {country : countryCapital }
    vecinos = []
    totalPopulation = countryPopulation

    #si tiene paises vecinos buscarlos
    if borderscountry:
        for border in borderscountry:
            borderData = await searchCountry(border)
            bordersCountrys.append(borderData)
        
        for border in bordersCountrys:
            nameNeighbor = border["name"]["common"]
            vecinos.append(nameNeighbor)
            languagesNeighbor = set(border.get("languages",{}).values())
            shared = countryLanguages.intersection(languagesNeighbor)
            comparacion[nameNeighbor] = list(shared)
            

            capitalNeighbor = border.get("capital")
            capitales[nameNeighbor] = capitalNeighbor
            populationNeighbor = border.get("population")
            totalPopulation += populationNeighbor

        json = {
            "PAIS BUSCADO" : country,
            "vecinos" : vecinos,
            "capitales": capitales,
            f"Lenguajes compartidos con {country}" : comparacion,
            "Suma de sus poblaciones" : totalPopulation 
        }
        return json
    else:
            json = {
            "PAIS BUSCADO" : country,
            "capital": capitales,
            "vecinos" : vecinos, 
            "poblacion total" : totalPopulation 
        }
            return json



