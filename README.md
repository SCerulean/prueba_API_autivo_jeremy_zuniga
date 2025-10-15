# prueba_API_autivo_jeremy_zuniga
Descripcion
---
Este proyecto Utiliza Fast API y uvicorn para generar una API Rest 
que genera datos personalizados que fueron solicitados, data extraida consumiendo la REST https://restcountries.com

Instalacion
---
Tener Python 3.8 minimo
Descargue el proyecto ya sea en zip o con git clone

Abra un terminal en la ruta del proyecto 

realice la instalacion de dependencias 
- pip install -r requirements.txt
- inicie el servidor local con el comando -->  uvicorn main:app --reload 

---
Endpoints disponibles
---

GET  http://127.0.0.1:8000/vecindad/{code}/neighbors
---
code = codigo cca3 del pais 

- Devuelve el pais solicitado 
- sus vecinos
- nombre de capital
- poblacion total  pais de busqueda + vecinos


---
GET  http://127.0.0.1:8000/rute//route?from={codeA}&to={codeB}
---
codeA, codeB = codigo cca3 del pais EJ: CHL

- devuelve si existe una ruta terrestre del pais a al pais b
- ruta  cca3 de los paises en orden mas corto para la ruta

---
GET  http://127.0.0.1:8000/{region}/stats
---
region = asia / americas / europa / africa / oceania

- CanJdad total de países en la región
- Población total y población promedio
- CanJdad total de idiomas únicos hablados en la región
- Top 5 países por población (nombre y población)

---
POST http://127.0.0.1:8000/countries/search
---
retorna los paises segun filtros enviados por body,  utilice postman, curl u otro

- todos los campos son opcionales
- formato del body: 
{

"minPopulaJon": 10000000,

"maxPopulaJon": 100000000,

"languages": ["Spanish", "English"],

"region": "Americas"
}

- minPopulaJon: países con población mayor o igual al valor
- maxPopulaJon: países con población menor o igual al valor
- languages: países que hablen AL MENOS uno de los idiomas especificados
- region: países que pertenezcan a la región especificada


