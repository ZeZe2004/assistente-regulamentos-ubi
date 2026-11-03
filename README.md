# Assistente de regulamentos da UBI

Aplicação web que encontra excertos de regulamentos públicos da UBI e mostra sempre o documento e a página. Projeto pessoal, sem ligação oficial à universidade.

**Experimentar:** https://zeze2004.github.io/assistente-regulamentos-ubi/

## Como funciona

- `backend/ingest.py` extrai o texto dos PDF e divide-o em excertos.
- `backend/search.py` e `frontend/src/search.ts` pesquisam os excertos com BM25.
- `backend/answer.py` pede ao modelo uma resposta baseada apenas nos excertos e devolve as fontes citadas.
- `backend/server.py` expõe a API, e `frontend/src/App.tsx` é a interface em React e TypeScript.
- `eval/avaliar.py` mede a pesquisa com perguntas fixas.

A versão publicada mostra só os excertos. As respostas com IA funcionam localmente, com uma chave da API.

Este projeto foi feito com a ajuda de um assistente de IA (Claude).

## Correr localmente

Pesquisa e avaliação, sem custos:

```
pip install -r requirements.txt
python backend/tests/test_search.py
python backend/tests/test_answer.py
python eval/avaliar.py
```

Respostas com IA: copia `.env.example` para `.env`, coloca a tua chave e corre:

```
uvicorn backend.server:app --reload
```

Noutro terminal:

```
cd frontend
npm install
set VITE_API_URL=http://localhost:8000
npm run dev
```

## Limitações

- O documento de avaliação e exames é uma imagem digitalizada, por isso ainda não entra na pesquisa.
- O documento de propinas é apenas a alteração de 2020.
- Os regulamentos podem ter versões mais recentes.
