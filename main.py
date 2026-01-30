from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Permitir que o site da Hostinger acesse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/buscar")
def buscar(produto: str):
    url = "https://api.mercadolibre.com/sites/MLB/search"
    params = {
        "q": produto,
        "limit": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    resultados = []

    for item in data["results"]:
        resultados.append({
            "nome": item["title"],
            "preco": item["price"],
            "link": item["permalink"] + "?matt_tool=seulinkafiliado",
            "imagem": item["thumbnail"]
        })

    return resultados
