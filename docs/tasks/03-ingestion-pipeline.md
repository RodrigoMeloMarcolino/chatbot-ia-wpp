# Fase 3 — Ingestion Pipeline

## Objetivo
Criar pipeline de ingestão: API → job (Redis) → worker → processamento →
persistência. Substituir o modelo atual de "drop de PDFs em pasta".

## Tarefas

### 3.1 Criar `ingestion/api.py`
- `POST /v1/ingestion/documents` — upload de arquivo
  - Aceitar `multipart/form-data`: file + source_id + metadata (JSON)
  - Criar `IngestionJob` com status `pending`
  - Salvar arquivo em disco (`/app/ingestion_staging/`)
  - Publicar job_id no Redis (`ingestion:queue`)
- `GET /v1/ingestion/jobs/{job_id}` — status do job
- `GET /v1/ingestion/jobs` — listar jobs com filtros

### 3.2 Criar `ingestion/worker.py`
- Worker assíncrono que consome da fila Redis (`ingestion:queue`)
- Para cada job:
  1. Atualizar status para `processing`
  2. Detectar tipo de arquivo (PDF, Markdown, TXT, etc.)
  3. Extrair texto
  4. Classificar documento (`generic_note`, `pdf`, `book_catalog`)
  5. Extrair metadados (frontmatter se Markdown, título, autor)
  6. Chunking (RecursiveCharacterTextSplitter)
  7. Gerar embeddings (OpenADA)
  8. Persistir: Document → DocumentVersion → Chunks → ChunkEmbeddings
  9. Atualizar job para `completed`
- Em caso de erro: `attempts++`, se > max → `failed`

### 3.3 Criar `ingestion/classifier.py`
- Classificador de documentos por tipo
- Regras:
  - PDF → `pdf`
  - Markdown com frontmatter `type: book_catalog` → `book_catalog`
  - Markdown genérico → `generic_note`
  - TXT → `generic_note`
  - Fallback: AI-assisted (LLM classifica se regra não cobre)

### 3.4 Configurar fila Redis
- Usar Redis existente (já no docker-compose)
- Lista `ingestion:queue` jobs pendentes
- Worker loop: `BLPOP` com timeout

### 3.5 Integrar com config.py
- Adicionar: `INGESTION_STAGING_DIR`, `INGESTION_WORKER_CONCURRENCY`,
  `INGESTION_MAX_ATTEMPTS`, `INGESTION_CHUNK_SIZE`,
  `INGESTION_CHUNK_OVERLAP`

## Critério de Aceitação
- [ ] Upload de PDF via API → job criado
- [ ] Worker processa o job e indexa o documento
- [ ] Documento indexado é consultável via `/v1/ask`
- [ ] Jobs com erro são marcados como `failed`
- [ ] Status dos jobs visível via `GET /v1/ingestion/jobs/{id}`

## Arquivos envolvidos
- **Criados:** `ingestion/api.py`, `ingestion/worker.py`,
  `ingestion/classifier.py`
- **Alterados:** `core/config.py`, `docker-compose.yaml` (workers),
  `app.py` (incluir rotas)
