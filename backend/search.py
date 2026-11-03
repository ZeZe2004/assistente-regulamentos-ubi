"""Pesquisa os excertos mais proximos de uma pergunta, com o algoritmo BM25."""
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

PARAGENS = set("a ao aos as com como da das de do dos e em na nas no nos o os ou para pela pelo por que se um uma".split())
K1, B = 1.5, 0.75


def tokens(texto):
    sem_acentos = unicodedata.normalize("NFKD", texto.lower())
    sem_acentos = "".join(c for c in sem_acentos if not unicodedata.combining(c))
    return [t for t in re.findall(r"[a-z0-9]+", sem_acentos) if t not in PARAGENS]


class Indice:
    def __init__(self, excertos):
        self.excertos = excertos
        self.contagens = [Counter(tokens(e["texto"])) for e in excertos]
        self.tamanhos = [sum(c.values()) for c in self.contagens]
        self.media = sum(self.tamanhos) / max(len(self.tamanhos), 1)
        self.presencas = Counter(t for c in self.contagens for t in c)

    def pesquisar(self, pergunta, quantos=3):
        total = len(self.excertos)
        resultados = []
        for i, contagem in enumerate(self.contagens):
            pontos = 0.0
            for termo in tokens(pergunta):
                freq = contagem[termo]
                if not freq:
                    continue
                n = self.presencas[termo]
                idf = math.log(1 + (total - n + 0.5) / (n + 0.5))
                pontos += idf * freq * (K1 + 1) / (freq + K1 * (1 - B + B * self.tamanhos[i] / self.media))
            if pontos > 0:
                resultados.append((pontos, self.excertos[i]))
        resultados.sort(key=lambda r: r[0], reverse=True)
        return resultados[:quantos]


if __name__ == "__main__":
    pergunta = " ".join(sys.argv[1:]) or sys.exit('Uso: python backend/search.py "a tua pergunta"')
    dados = json.loads(Path("data/index.json").read_text(encoding="utf-8"))
    for pontos, e in Indice(dados).pesquisar(pergunta):
        print(f"[{pontos:.2f}] {e['documento']}, p. {e['pagina']}\n{e['texto'][:300]}...\n")
