# Assistente de regulamentos da UBI

Aplicação que responde a perguntas sobre regulamentos públicos da UBI e mostra de onde tirou cada resposta.

Estado atual: leitura dos PDF e pesquisa de excertos. Ainda não tem modelo de IA nem interface.

## Experimentar

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python backend/ingest.py
python backend/search.py "Até quando posso pagar as propinas?"
python backend/tests/test_search.py
```

Antes, coloca os PDF indicados em `docs/fontes.md` na pasta `data/pdfs/`.
