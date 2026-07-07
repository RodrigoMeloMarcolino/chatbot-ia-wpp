# Fase 2 — Hybrid RAG

## Objetivo
Evoluir o RAG naive (apenas similaridade vetorial) para RAG híbrido
com busca semântica (pgvector) + busca textual (PostgreSQL FTS) +
reranking.

## Tarefas

### 2.1 Criar `rag/hybrid_retriever.py`
- Retriever que combina:
  - **pgvector ANN:** busca por similaridade coseno (HNSW index)
  - **PostgreSQL FTS:** busca textual com `to_tsvector`/`plainto_tsquery`
  - **Weighted sum:** combinar scores (ex: 0.7 semântico + 0.3 textual)
- Suporte a metadata filters (source_id, document_type, etc.)
- `top_k` configurável (default 5 para /ask, 10 para /search)
- Preservar source grounding (document_id, title, score)

### 2.2 Opcional: Re-ranker
- Implementar reranking com `cross-encoder/ms-marco-MiniLM-L-6-v2`
  ou similar (pode ser via API ou local)
- Re-rank dos top-K resultados do retrieval híbrido
- Pode ser adiado se o custo/complexidade for alto no MVP

### 2.3 Criar rota `POST /v1/ask`
- Receber `{ question, filters, top_k }`
- Chamar hybrid_retriever
- Montar contexto com chunks + fontes
- Chamar LLM (RAG chain)
- Retornar `{ answer, sources, tokens_used, estimated_cost_usd }`

### 2.4 Criar rota `POST /v1/search`
- Receber `{ query, filters, top_k }`
- Chamar hybrid_retriever
- Retornar chunks com metadados e scores
- Sem chamada de LLM (busca pura)

### 2.5 Atualizar `rag/chains.py`
- Refatorar chain existente para usar o hybrid_retriever
- Prompt do sistema adaptado para incluir fontes/citações
- Logging de tokens e custo estimado

### 2.6 Token/cost logging
- Calcular tokens de input (contexto + pergunta) e output (resposta)
- Estimar custo com base no modelo usado
- Incluir no response do `/v1/ask`

## Critério de Aceitação
- [ ] `/v1/ask` retorna resposta com markdown e citações
- [ ] `/v1/search` retorna chunks sem LLM
- [ ] Busca textual encontra termos exatos que semântica perde
- [ ] Busca semântica encontra conceitos que FTS perde
- [ ] Metadata filters funcionam (ex: filtrar por source)
- [ ] Token/cost logging presente no response

## Arquivos envolvidos
- **Criados:** `rag/hybrid_retriever.py`
- **Alterados:** `rag/chains.py`, `rag/prompts.py`
- **Rota:** adicionar em `app.py` ou `routers/rag.py` (se router existir)
