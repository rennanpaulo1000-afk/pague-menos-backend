from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

AFILIADO_ML = ""  # depois você coloca seu código de afiliado aqui

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Backend rodando com sucesso 🚀"}

@app.get("/buscar")
def buscar(produto: str):
    url = "https://api.mercadolibre.com/sites/MLB/search"

    params = {
        "q": produto,
        "limit": 10
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        resultados = []

        if "results" not in data:
            return {
                "erro": "Resposta inesperada do Mercado Livre",
                "resposta": data
            }

        for item in data["results"]:
            resultados.append({
                "nome": item.get("title"),
                "preco": item.get("price"),
                "link": item.get("permalink"),
                "imagem": item.get("thumbnail")
            })

        return resultados

    except Exception as e:
        return {
            "erro": "Falha ao buscar produtos",
            "detalhe": str(e)
        }
