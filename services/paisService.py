import httpx
from collections import deque
from .models import CountryFilter

BASE_URL = "https://restcountries.com/v3.1"
COUNTRYS_URL= "https://restcountries.com/v3.1/alpha"
REGIONS_URL = "https://restcountries.com/v3.1/region"


#busqueda por pais 
async def searchCountry(code, params : str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{COUNTRYS_URL}/{code}?fields={params}")

        if response.status_code != 200:
            return {"error" : f" no se encontro el pais '{code}'"}
        data = response.json()
        return data


#busqueda por region
async def searchRegion(Region, params : str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{REGIONS_URL}/{Region}?fields={params}")

        if response.status_code != 200:
            return {"error" : f" no se encontro la region '{Region}'"}
        data = response.json()
        return data
    
    

async def neighbors(code):
    mainCountry = await searchCountry(code, "name,borders,population,capital,languages")

    if not mainCountry:
        return None
    
    bordersCountrys = []

    #separar la data del pais buscado
    country = mainCountry["name"]["common"]
    countryLanguages = set(mainCountry.get("languages",{}).values())
    countryPopulation = mainCountry.get("population")
    countryCapital = mainCountry.get("capital")
    borderscountry = mainCountry.get("borders",[])



    sharedLanguages = {} #
    capitales = {country : countryCapital } # lista de capitales
    vecinos = []
    totalPopulation = countryPopulation

    #si tiene paises vecinos busca su data y la agrega a la lista correspondiente
    if borderscountry:
        #buscar por cada uno
        for border in borderscountry:
            borderData = await searchCountry(border,"name,borders,population,capital,languages")
            bordersCountrys.append(borderData)
        

        for border in bordersCountrys:      
            nameNeighbor = border["name"]["common"]
            vecinos.append(nameNeighbor)  #agrega de paises vecinos del pais de busqueda  a la lista

            languagesNeighbor = set(border.get("languages",{}).values())
            shared = countryLanguages.intersection(languagesNeighbor)
            sharedLanguages[nameNeighbor] = list(shared)   #agrega   lenguajes compartidos con el pais de busqueda

            capitalNeighbor = border.get("capital")
            capitales[nameNeighbor] = capitalNeighbor #agrega capitales a la lista

            populationNeighbor = border.get("population")
            totalPopulation += populationNeighbor #poblacion total

        json = {
            "PAIS BUSCADO" : country,
            "vecinos" : vecinos,
            "capitales": capitales,
            f"Lenguajes compartidos con {country}" : sharedLanguages,
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


# devuelve la ruta mas corta de a y b si existe ruta terrestre  
async def RuteCountryAtoB(codeA , codeB):

    #extracion de datos del pais A
    paisA = await searchCountry(codeA,"name,borders,region,cca3")
    bordersA = paisA.get("borders",[])
    regionA = paisA.get("region")

    #extracion de datos del pais B 
    paisB = await searchCountry(codeB,"name,borders,region,cca3")
    bordersB = paisB.get("borders",[])
    regionB = paisB.get("region")

    #omite si no hay vecinos
    if not bordersA:
        return {"mensaje": f"no hay ruta terrestre {paisA["name"]["common"]} no limita con nadie"}

    if not bordersB:
        return {"mensaje": f"no hay ruta terrestre {paisB["name"]["common"]} no limita con nadie"}
    
    #permite agregar al grafo los paises en RegionCountrys en formato "nombre" :"[vecinos]" (nombre en cca3)
    grafo = {}
    def AppendGrafoCountrys(RegionCountrys):
        print(RegionCountrys)
        for country in RegionCountrys:
                    name = country["cca3"]
                    borders = country["borders"]
                    grafo[name] = borders
    
    #busca todos los paises de la region donde se encuentran los pais A Y B y usa la funcion  AppendGrafoCountrys 
    if regionA == regionB:
        RegionCountrys = await searchRegion(regionA,"name,borders,cca3")
        AppendGrafoCountrys(RegionCountrys)
        
      
    else:
        RegionCountrysA = await searchRegion(regionA,"name,borders,cca3")
        RegionCountrysB = await searchRegion(regionB,"name,borders,cca3")
        AppendGrafoCountrys(RegionCountrysA)
        AppendGrafoCountrys(RegionCountrysB)
        


    # utiliza deque para encontrar la ruta mas corta segun los paises en el grafo generado
    queue = deque([[codeA]])
    visited = set()

    while queue:
        path = queue.popleft()
        country = path[-1]

        if country == codeB:
            # Si llega al  destino retorna
            return {"ruta": path, "hay_ruta": True}

        if country not in visited:
            visited.add(country)
            for neighbor in grafo[country]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    # Si no se encontró camino terrestre
    return {"ruta": None, "hay_ruta": False}



#Fucion 3
# devuelve las metricas solicitadas
async def regionMetrics(regioncCode):
    countrys = await searchRegion(regioncCode,"name,population,languages")

    totalCountrys = 0 
    totalPopulation = 0
    uniqueLanguage = []
    top5 = sorted(countrys, key=lambda x: x["population"], reverse=True)[:5] #ordena y selecciona los 5 con mayor poblacion
    top = {}


    for country in countrys:
        totalCountrys += 1
        totalPopulation += country["population"]
        languages = set(country.get("languages",{}).values())

        #agrega lenguajes unicos
        for language in languages:
             if language not in uniqueLanguage:
                  uniqueLanguage.append(language)

    #modifica el top a "nombre": "poblacion"
    for country in top5:
         top[country["name"]["common"]] = country["population"]

    # probmedio poblacion
    averagePopulation = totalPopulation//totalCountrys

    json = {
         "Region solicitada": regioncCode,
         "total paises" : totalCountrys,
         "Poblacion total": totalPopulation,
         "Poblacion promedio" : averagePopulation,
         "lenguajes unicos": uniqueLanguage,
         "top 5 paises con mas poblacion": top
    }

    return json

 

# Permite filtrar los datos  segun region lenguaje y poblacion
async def advancedSearch(filters : CountryFilter):
    print(filters.region)
    countrys = await searchRegion(filters.region,"population,languages,name,cca3,region")

    result = []
    totalCount = 0 
    for country in countrys:
        population = country.get("population")
        language = set(country.get("languages",{}).values())
        reg = country.get("region")

        if   filters.minPopulation and population < filters.minPopulation:
             continue
        if   filters.maxPopulation and population > filters.maxPopulation:
             continue
        if filters.languages and not language.intersection(filters.languages):  
             continue
        

        result.append({
            "name": country["name"]["common"],
            "code": country["cca3"],
            "population": population,
            "region": reg,
            "languages": list(language)
        })
        totalCount +=1
        
    json = {
         "Total resultados" : totalCount,
         "paises" : result
    }
    return json


    
    



        

    
