# ADR-004: RAG híbrido com reranking

## Status
Aceito.

## Contexto
O RAG original usava apenas similaridade vetorial (ChromaDB + OpenAI embeddings).
Isso perdia matches por termos exatos (nomes próprios, códigos, siglas) e
não tinha mecanismo de refinamento dos resultados.

## Decisão
Implementar RAG híbrido com três estágios:
1. **Semântico:** busca ANN no pgvector (cosine similarity)
2. **Textual:** PostgreSQL full-text search com `ts_rank`
3. **Reranking:** weighted sum dos scores (0.7 semântico + 0.3 textual)
   + opcional cross-encoder para reranking fino

## Consequências
**Positivas:**
- Recupera documentos por similaridade de conceito E por termo exato
- Metadata filters (source_id, document_type) aplicados em ambos os estágios
- Reranking melhora precisão do contexto final
- TSVECTOR em `documents` e `chunks` é gerado automaticamente (computed column)

**Negativas:**
- Mais complexo que busca vetorial pura
- Cross-encoder adiciona latência e custo (pode ser desligado no MVP)
- Requer tuning dos pesos

## Alternativas consideradas
- **Só busca vetorial:** simples, mas perde recall em termos exatos
- **Só FTS:** simples, mas perde sinônimos e conceitos
- **RAG fusion:** combina resultados com reciprocal rank fusion (simplificação
  do weighted sum)
