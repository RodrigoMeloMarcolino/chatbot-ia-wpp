# Fase 7 — Book Catalog Module

## Objetivo
Implementar o primeiro módulo especializado: catálogo de livros.
Permite catalogar livros a partir de documentos (Markdown, Notion),
enriquecer metadados e linkar assets relacionados.

## Tarefas

### 7.1 Modelos do módulo
Em `modules/books/models.py`:
- `Book`: id, title, normalized_title, subtitle, author, isbn, status,
  topics (JSONB), tags (JSONB), metadata (JSONB), created_at, updated_at
- `BookSource`: id, book_id, source_document_id, source_type, source_uri,
  confidence, metadata, created_at
- `BookAsset`: id, book_id, asset_id, document_id, asset_type, uri,
  ingestion_status, metadata, created_at, updated_at
- `BookEnrichmentJob`: id, book_id, status, provider, attempts,
  last_error, metadata, created_at, updated_at

### 7.2 Detector de book_catalog na ingestion
- Em `ingestion/classifier.py`, adicionar regra:
  - Markdown/Notion com frontmatter `type: book_catalog` ou
    título contendo "Catálogo de Livros"
- Ao detectar, além da indexação genérica:
  1. Extrair entradas de livro do documento
  2. Persistir ou atualizar Book entities
  3. Criar relações book → source_document

### 7.3 Extrator de livros
Em `modules/books/extractor.py`:
- Extrair livros de Markdown estruturado:
  - Formato tabela: `| Título | Autor | ISBN | Status |`
  - Formato lista: `- [x] Clean Architecture (Robert Martin)`
  - Frontmatter com array de livros
- Para cada livro:
  1. Normalizar título
  2. Buscar entidade existente (evitar duplicata)
  3. Criar ou atualizar entidade `book`
  4. Criar relação `book → source_document`

### 7.4 Ferramentas do agente para catálogo
Em `agents/tools/catalog_tools.py` (expandir):
- `search_books(query, author, status)` — busca no catálogo
- `extract_books_from_document(document_id)` — força extração
- `fetch_book_metadata(isbn, title, author)` — enriquecimento público
  (Open Library API ou Google Books API)
- `link_book_to_document(book_id, document_id, relationship)` —
  associa nota/PDF ao livro

### 7.5 Rotas da API do módulo
- `GET /v1/books` — listar catálogo com filtros
- `GET /v1/books/{id}` — detalhe + assets relacionados
- `PATCH /v1/books/{id}` — atualizar metadados
- `POST /v1/books/{id}/enrich` — trigger enriquecimento externo

## Critério de Aceitação
- [ ] Documento book_catalog é detectado na ingestion
- [ ] Livros são extraídos e persistidos como entidades
- [ ] Catálogo consultável via API
- [ ] Agente consegue buscar livros
- [ ] Relações livro → documento de origem criadas

## Arquivos envolvidos
- **Criados:** `modules/books/models.py`, `modules/books/extractor.py`,
  `modules/books/router.py`
- **Alterados:** `ingestion/classifier.py`, `agents/tools/catalog_tools.py`,
  `app.py` (incluir rotas)
