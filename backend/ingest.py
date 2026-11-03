"""Extrai o texto dos PDF e divide-o em excertos com documento e pagina."""
import json
import sys
from pathlib import Path

from pypdf import PdfReader

TAMANHO = 120  # palavras por excerto
SOBREPOSICAO = 30  # palavras repetidas entre excertos seguidos


def dividir(texto, tamanho=TAMANHO, sobreposicao=SOBREPOSICAO):
    palavras = texto.split()
    passo = tamanho - sobreposicao
    excertos = []
    for inicio in range(0, len(palavras), passo):
        parte = palavras[inicio:inicio + tamanho]
        if parte:
            excertos.append(" ".join(parte))
        if inicio + tamanho >= len(palavras):
            break
    return excertos


def ler_pdf(caminho):
    excertos = []
    for numero, pagina in enumerate(PdfReader(caminho).pages, start=1):
        texto = pagina.extract_text() or ""
        for parte in dividir(texto):
            excertos.append({"documento": Path(caminho).name, "pagina": numero, "texto": parte})
    return excertos


def main(pasta="data/pdfs", saida="data/index.json"):
    excertos = []
    for pdf in sorted(Path(pasta).glob("*.pdf")):
        lidos = ler_pdf(pdf)
        print(f"{pdf.name}: {len(lidos)} excertos")
        excertos.extend(lidos)
    if not excertos:
        sys.exit(f"Nenhum PDF encontrado em {pasta}")
    Path(saida).write_text(json.dumps(excertos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Total: {len(excertos)} excertos em {saida}")


if __name__ == "__main__":
    main()
