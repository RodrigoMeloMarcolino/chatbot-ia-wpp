# PRD — Second Brain

**Origem:** chatbot-ia-wpp
**Status:** Planejamento
**Livedoc:** Second Brain - LiveDoc (Google Docs)

## 1. Visão Geral

Evoluir o `chatbot-ia-wpp` (WhatsApp chatbot com RAG + LangGraph) para o
**Second Brain**, um sistema pessoal e auto-hospedado de conhecimento com
RAG híbrido, conhecimento estruturado, pipeline de ingestão, agentes
orquestradores e módulos especializados.

Tudo no **mesmo repositório e deploy** — sem separação de serviços.

## 2. Princípios

- **Auto-hospedado:** tudo roda em VPS/infra própria com Docker Compose.
- **Evolução incremental:** cada fase produz um sistema funcional e testável.
- **Custo consciente:** PostgreSQL + pgvector, evitar serviços gerenciados.
- **Modular:** core genérico; módulos especializados plugam por contratos.
- **Pronto para agentes:** agentes acessam o sistema via APIs/tools explícitas.
- **Projeto de portfólio:** testes, type hints, lint, ADRs, README impecáveis.

## 3. Stack Tecnológica

| Componente | Tecnologia |
|------------|-----------|
| Runtime | Python 3.13, FastAPI |
| Banco principal | PostgreSQL 15 |
| Vector store | pgvector (HNSW index) |
| ORM | SQLAlchemy 2.x async |
| Embeddings | OpenAI `text-embedding-3-small` |
| LLM | OpenAI GPT-4o / GPT-4o-mini |
| Agent framework | LangGraph |
| Queue | Redis (já existente) |
| Containers | Docker Compose |
| Canal | WhatsApp (Evolution API) |
| Connector inicial | Notion API |
| Web UI (futuro) | Streamlit |

## 4. Arquitetura (Monorepo)

```
chatbot-ia-wpp/
├── app.py                 # FastAPI entrypoint (webhook + APIs)
├── core/                  # Domínio central
│   ├── models.py          # SQLAlchemy models (9 tabelas)
│   ├── database.py        # Engine async + session
│   └── config.py          # (expandido do original)
├── rag/                   # Motor RAG híbrido
│   ├── hybrid_retriever.py
│   ├── chains.py          # (refatorado)
│   └── prompts.py         # (refatorado)
├── ingestion/             # Pipeline de ingestão
│   ├── api.py             # POST /v1/ingestion/documents
│   ├── worker.py          # Processador assíncrono
│   └── connectors/
│       └── notion.py      # Conector Notion
├── agents/                # LangGraph orquestrador
│   ├── graph.py           # (refatorado)
│   ├── nodes.py           # (refatorado)
│   ├── state.py           # (refatorado)
│   └── tools/             # Tools do Second Brain
│       ├── rag_tools.py
│       ├── ingestion_tools.py
│       └── catalog_tools.py
├── modules/               # Módulos especializados
│   └── books/             # Book Catalog (futuro)
├── whatsapp/              # Integração WhatsApp
│   ├── webhook.py         # (extraído de app.py)
│   ├── message_buffer.py  # (existente)
│   └── evolution_api.py   # (existente)
├── docs/
│   ├── PRD.md
│   ├── tasks/
│   └── adr/
├── tests/
│   ├── unit/
│   └── integration/
├── docker-compose.yaml    # (expandido: postgres + pgvector + redis)
├── Dockerfile
└── requirements.txt
```

## 5. Modelo de Dados

9 tabelas no PostgreSQL com pgvector:

| Tabela | Função |
|--------|--------|
| `sources` | Fontes configuradas (Notion, filesystem, manual) |
| `documents` | Documentos normalizados com FTS via `search_vector TSVECTOR` |
| `document_versions` | Versões processadas dos documentos |
| `chunks` | Segmentos de texto recuperáveis |
| `chunk_embeddings` | Embeddings vetoriais (HNSW index) |
| `ingestion_jobs` | Jobs da fila de processamento |
| `entities` | Entidades estruturadas (book, author, project, etc.) |
| `relations` | Relacionamentos entre entidades |
| `assets` | Arquivos referenciados (PDF, EPUB, etc.) |

### Características principais

- **RAG híbrido**: `search_vector TSVECTOR` (FTS) + `embedding vector` (semântico) + reranking
- **Idempotência**: `UNIQUE(source_id, canonical_uri)` em documentos
- **Hierarquia**: `documents.parent_id` para aninhamento (Notion database > páginas)
- **Múltiplos modelos**: `UNIQUE(chunk_id, embedding_model)` em embeddings
- **HNSW index**: busca vetorial mais rápida que IVFFlat para nosso volume
- **JSONB**: metadados flexíveis com índices GIN

## 6. Fases de Implementação

### Fase 1 — Core Migration
Trocar ChromaDB por PostgreSQL + pgvector. Criar models, database, migrar vectorstore.

**Tasks:** 6
**Resultado:** RAG funcionando sobre pgvector.

### Fase 2 — Hybrid RAG
Implementar retriever híbrido (pgvector + FTS + reranker). Endpoints `/v1/ask` e `/v1/search`.

**Tasks:** 4
**Resultado:** RAG com citações e busca textual + semântica.

### Fase 3 — Ingestion Pipeline
API de ingestão + worker assíncrono com fila Redis. Remover "drop de PDFs" manual.

**Tasks:** 4
**Resultado:** Upload via API → worker indexa → disponível em < 2min.

### Fase 4 — Notion Connector
Conectar ao Notion API, sync de páginas e databases, classificação de documentos.

**Tasks:** 3
**Resultado:** Notion como fonte de conhecimento.

### Fase 5 — Agent Orchestrator
LangGraph como orquestrador com tools: `ask_rag`, `search_documents`, `trigger_ingestion`, etc.

**Tasks:** 3
**Resultado:** Agente WhatsApp opera o sistema completo.

### Fase 6 — Conhecimento Estruturado
API de entities, relations, assets. Tools do agente para criar/consultar.

**Tasks:** 3
**Resultado:** Grafo de conhecimento consultável.

### Fase 7 — Book Catalog
Primeiro módulo especializado. Tabelas, extrator, tools do agente.

**Tasks:** 4
**Resultado:** Catálogo de livros funcional.

### Fase 8 — Portfolio Polish
README, ADRs, testes, CI, lint impecável.

**Tasks:** 3
**Resultado:** Projeto pronto para portfólio.

### Fase 9 — Web UI (Streamlit)
Chat, jobs, custos, book catalog.

**Tasks:** 4
**Resultado:** Interface web completa.

## 7. Contratos de API (MVP)

### POST /v1/ask

```json
{
  "question": "o que é tal coisa?",
  "filters": { "sources": ["notion"], "document_types": ["note"] },
  "top_k": 5
}
```

Response:

```json
{
  "answer": "resposta com markdown e citações",
  "sources": [
    { "document_id": "uuid", "title": "Nota sobre X", "chunk": "trecho relevante", "score": 0.95 }
  ],
  "tokens_used": 1234,
  "estimated_cost_usd": 0.002
}
```

### POST /v1/search

```json
{
  "query": "termo de busca",
  "filters": {},
  "top_k": 10
}
```

### POST /v1/ingestion/documents

`multipart/form-data` com `file` + `source_id` + `metadata` JSON

### POST /v1/entities

```json
{
  "entity_type": "book",
  "canonical_name": "Clean Architecture",
  "metadata": {}
}
```

## 8. Critérios de Sucesso

- **F1:** RAG responde perguntas com retrieval do pgvector. ChromaDB removido.
- **F2:** `/v1/ask` retorna respostas com citações; busca híbrida funciona.
- **F3:** Upload de documento via API → worker indexa → consultável.
- **F4:** Notion sync funcional.
- **F5:** Agente WhatsApp consegue perguntar, buscar e triggerar ingestão.
- **F6:** API de entidades e relações operacional.
- **F7:** Catálogo de livros funcional com tools do agente.
- **F8:** `make lint`, `make test`, `make typecheck` passam.
- **F9:** Web UI com chat, fontes, ingestion status e custos.

## 9. Não Escopo (MVP)

- CLI dedicada
- Kubernetes / k3s
- Autenticação multi-usuário
- Plugin Obsidian dedicado
- Conectores externos como repositórios separados
- MinIO / object storage externo
