"""Servidor da API. Corre com: uvicorn backend.server:app --reload"""
import json
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent))
from answer import responder
from search import Indice

load_dotenv()
RAIZ = Path(__file__).resolve().parents[1]
indice = Indice(json.loads((RAIZ / "frontend/public/index.json").read_text(encoding="utf-8")))
app = FastAPI(title="Assistente de regulamentos da UBI")
app.add_middleware(CORSMiddleware, allow_origins=os.environ.get("ORIGENS", "http://localhost:5173").split(","), allow_methods=["POST"], allow_headers=["*"])


class Pedido(BaseModel):
    pergunta: str = Field(min_length=3, max_length=500)


@app.post("/api/perguntar")
def perguntar(pedido: Pedido):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(503, "Falta configurar a chave da API.")
    try:
        return responder(pedido.pergunta, indice, anthropic.Anthropic())
    except anthropic.APIError as erro:
        raise HTTPException(502, "O serviço de IA falhou. Tenta outra vez.") from erro
