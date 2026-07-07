# Fase 1 — Core Migration (pgvector + modelos de dados)

## Objetivo
Substituir ChromaDB por PostgreSQL + pgvector e criar a base de dados
conforme o modelo do livedoc.

## Pré-requisitos
- Docker Compose instalado
- Imagem `pgvector/pgvector:pg15` disponível

## Tarefas

### 1.1 Criar `core/database.py`
- Engine SQLAlchemy async com `asyncpg`
- `DATABASE_URL` via variável de ambiente
- `Base` declarativa
- `async_session_factory`
- `init_db()` para criar tabelas
- `get_session()` como generator assíncrono

### 1.2 Criar `core/models.py`
- 9 tabelas: Source, Document, DocumentVersion, Chunk, ChunkEmbedding,
  IngestionJob, Entity, Relation, Asset
- `search_vector TSVECTOR` em Document e Chunk (FTS)
- Índices GIN, HNSW, UniqueConstraints
- Relationships entre modelos

### 1.3 Atualizar `docker-compose.yaml`
- Adicionar serviço `postgres` com `pgvector/pgvector:pg15`
- Porta 5432, volume persistente (`postgres_data`)
- Health check
- `DATABASE_URL` no serviço `bot`
- Dependência `bot -> postgres`

### 1.4 Criar `core/pgvector_store.py`
- Substituir `vectorstore.py` (ChromaDB)
- Implementar PGVector como vector store do LangChain
- Manter interface `get_vectorstore()` (retriever)
- Configurar collection_name, embedding function

### 1.5 Atualizar `core/config.py`
- Adicionar `DATABASE_URL`
- Remover `VECTOR_STORE_PATH` (ChromaDB)
- Manter demais configurações

### 1.6 Atualizar dependências
- **Remover:** `chromadb`, `langchain-chroma`
- **Adicionar:** `asyncpg`, `psycopg2-binary`, `langchain-postgres`, `pgvector`,
  `sqlalchemy[asyncio]`

### 1.7 Remover código legado
- Remover arquivo `vectorstore.py` (antigo)
- Remover diretório `vectorstore/` (dados ChromaDB)

### 1.8 Testar integração
- Subir stack: `docker compose up -d postgres redis`
- Verificar tabelas criadas no PostgreSQL
- Subir bot
- Enviar mensagem no WhatsApp → resposta via pgvector

## Nota de encerramento
A fase 1 foi concluída com uma simplificação arquitetural: em vez de manter um esquema relacional de domínio customizado (`sources`, `documents`, `chunks`, `chunk_embeddings`) mais o vectorstore do LangChain, optou-se por usar **apenas o `PGVector` nativo do LangChain** (`langchain_postgres`). Isso reduz complexidade, evita duplicação de dados e alinha o projeto ao padrão de mercado. O esquema de domínio foi removido e será revisitado no módulo de ingestion pipeline (Fase 3).

## Critério de Aceitação
- [x] ChromaDB removido do projeto
- [x] PostgreSQL + pgvector configurados no Docker Compose
- [x] RAG responde perguntas com retrieval do pgvector
- [x] `core/pgvector_store.py` mantém a interface `get_vectorstore()`
- [x] `init_db()` e modelos SQLAlchemy removidos (escopo transferido para Fase 3)

## Arquivos envolvidos
- **Criados:** `core/pgvector_store.py`
- **Alterados:** `core/config.py`, `docker-compose.yaml`, `requirements.txt`, `app.py`
- **Removidos:** `vectorstore.py`, `vectorstore/`, `core/database.py`, `core/models.py`, `scripts/test_db_connection.py`, `ingestion/`
