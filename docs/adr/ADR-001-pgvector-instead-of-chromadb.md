# ADR-001: Pgvector como vector store

## Status
Aceito.

## Contexto
O chatbot-ia-wpp original usava ChromaDB como vector store. O Second Brain
precisa de um modelo de dados relacional com suporte a consultas híbridas,
metadados estruturados e integridade transacional.

## Decisão
Substituir ChromaDB por PostgreSQL + extensão pgvector.

## Consequências
**Positivas:**
- Dados relacionais e vetoriais no mesmo banco (sem split brain)
- Transações ACID entre chunks, embeddings, documentos e metadados
- Full-text search nativo (TSVECTOR + GIN) para RAG híbrido
- HNSW index para busca vetorial eficiente
- Menos componentes na stack (remove ChromaDB)

**Negativas:**
- Perde a simplicidade do ChromaDB (banco embeddado, zero config)
- Requer migração dos dados existentes (ou recriação)
- pgvector pode ser menos performante que Milvus/Pinecone em escala muito grande

## Alternativas consideradas
- **Manter ChromaDB + PostgreSQL separado:** complexidade extra, sem integridade
  referencial entre chunks e documentos
- **Qdrant:** vector store dedicado, mas adiciona mais um serviço
- **Pinecone:** serviço gerenciado, viola princípio self-hosted
