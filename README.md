# Assistente de regulamentos da UBI

Aplicação web que encontra excertos de regulamentos públicos da UBI e mostra sempre o documento e a página. Projeto pessoal, sem ligação oficial à universidade.

**Experimentar:** https://zeze2004.github.io/assistente-regulamentos-ubi/

## Como funciona

- `backend/ingest.py` extrai o texto dos PDF e divide-o em excertos.
- `frontend/src/search.ts` pesquisa os excertos com BM25 e reduz as palavras à raiz.
- `frontend/src/App.tsx` é a interface, em React e TypeScript.

Ainda não usa um modelo de IA: mostra os excertos relevantes, sem redigir respostas.

Este projeto foi feito com a ajuda de um assistente de IA (Claude).

## Correr localmente

```
cd frontend
npm install
npm test
npm run dev
```

Para gerar o índice de novo, coloca os PDF de `docs/fontes.md` em `data/pdfs/`, corre `python backend/ingest.py` e copia `data/index.json` para `frontend/public/`.

## Limitações

- O documento de avaliação e exames é uma imagem digitalizada, por isso ainda não entra na pesquisa.
- O documento de propinas é apenas a alteração de 2020.
- Os regulamentos podem ter versões mais recentes.
