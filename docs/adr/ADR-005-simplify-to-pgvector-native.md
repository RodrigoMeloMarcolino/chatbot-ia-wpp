# ADR-005: Simplificar para PGVector nativo do LangChain

## Status
Aceito.

## Contexto
Durante a Fase 1 (Core Migration) foram modeladas 9 tabelas de domínio (`sources`, `documents`, `document_versions`, `chunks`, `chunk_embeddings`, `ingestion_jobs`, `entities`, `relations`, `assets`) com SQLAlchemy + pgvector. O objetivo era ter metadados ricos, versionamento e integridade referencial entre documentos e seus embeddings.

Após testes práticos, verificou-se que:
- O `seed_vectorstore.py` populava tanto as tabelas de domínio quanto a tabela `langchain_pg_embedding` do `PGVector`, gerando duplicação de dados.
- O retriever do LangChain (`PGVector.as_retriever()`) lê apenas da tabela `langchain_pg_embedding`.
- Manter as duas fontes exigiria escrever uma vectorstore customizada ou sincronização constante, aumentando a complexidade do MVP.

## Decisão
Usar apenas o `PGVector` do `langchain-postgres` como vectorstore. As tabelas de domínio foram removidas do escopo do RAG e serão revisitadas no módulo de ingestion pipeline (Fase 3), onde a deduplicação por hash de conteúdo e metadados estruturados serão implementados.

## Consequências
**Positivas:**
- Menor complexidade no código (sem modelos SQLAlchemy customizados, sem retriever customizado)
- Alinhamento com o padrão de mercado do ecossistema LangChain
- Uma única fonte de verdade para embeddings (`langchain_pg_embedding`)
- Menor superfície de manutenção

**Negativas:**
- Perde o versionamento de documentos nativo
- Perde a integridade referencial entre documentos e chunks
- Metadados avançados (source, entity, relation) ficam para uma fase futura

## Alternativas consideradas
- **Manter esquema de domínio + PGVector (dual-write):** rejeitado por duplicar dados e complexidade
- **Escrever vectorstore customizada lendo de `chunk_embeddings`:** rejeitado por reimplementar funcionalidade já disponível no framework
- **Usar `langchain-postgres` v2 com tabelas customizadas:** rejeitado por API instável e pouca documentação
