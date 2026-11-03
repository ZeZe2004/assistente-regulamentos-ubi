"""Mede a pesquisa e, com --ia, gera respostas para rever à mão.

python eval/avaliar.py       (sem custos)
python eval/avaliar.py --ia  (gasta créditos da API)
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "backend"))
from answer import PONTUACAO_MINIMA, responder
from search import Indice

indice = Indice(json.loads((RAIZ / "frontend/public/index.json").read_text(encoding="utf-8")))
casos = json.loads((RAIZ / "eval/perguntas.json").read_text(encoding="utf-8"))
certos = 0
for c in casos:
    top = [e for p, e in indice.pesquisar(c["pergunta"], 5) if p >= PONTUACAO_MINIMA]
    if c["documento"] is None:
        ok = not top
    else:
        ok = any(e["documento"] == c["documento"] and c["termo"] in e["texto"].lower() for e in top)
    certos += ok
    print(("OK   " if ok else "FALHA"), c["pergunta"])
print(f"Pesquisa: {certos}/{len(casos)}")

if "--ia" in sys.argv:
    import anthropic
    from dotenv import load_dotenv

    load_dotenv(RAIZ / ".env")
    cliente = anthropic.Anthropic()
    entrada = saida = 0
    for c in casos:
        r = responder(c["pergunta"], indice, cliente)
        entrada += r["tokens"]["entrada"]
        saida += r["tokens"]["saida"]
        print(f"\nP: {c['pergunta']}\nR: {r['resposta']}\nFontes: {[(f['documento'], f['pagina']) for f in r['fontes']]}")
    print(f"\nTokens: {entrada} de entrada, {saida} de saída")
