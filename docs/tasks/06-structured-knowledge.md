# Fase 6 — Conhecimento Estruturado (Entities, Relations, Assets)

## Objetivo
Implementar a camada de conhecimento estruturado com entidades,
relacionamentos e assets, conforme o modelo do livedoc.

## Tarefas

### 6.1 CRUD de Entities
- `POST /v1/entities` — criar entidade
- `GET /v1/entities` — listar com filtros (entity_type, search)
- `GET /v1/entities/{id}` — detalhe da entidade
- `PATCH /v1/entities/{id}` — atualizar
- `DELETE /v1/entities/{id}` — deletar (com limpeza de relations)
- Validação de `entity_type` contra valores permitidos
- `normalized_name` gerado automaticamente (lowercase, sem acentos)

### 6.2 CRUD de Relations
- `POST /v1/relations` — criar relação
- `GET /v1/relations` — listar com filtros (source, target, relation_type)
- `DELETE /v1/relations/{id}` — deletar
- UniqueConstraint bidirecional evita duplicatas
- Validação de `relation_type` contra valores permitidos

### 6.3 CRUD de Assets
- `POST /v1/assets` — registrar asset
- `GET /v1/assets` — listar
- `DELETE /v1/assets/{id}` — deletar
- `UNIQUE(uri)` garante idempotência

### 6.4 Ferramentas do agente
- `agents/tools/catalog_tools.py` (preparatório para módulos):
  - `search_entities(entity_type, query)` — busca por tipo
  - `create_entity(entity_type, canonical_name, metadata)` — registra entidade
  - `link_entity_to_document(entity_id, document_id)` — cria relação
- Ferramentas registradas no LangGraph

### 6.5 Integração com ingestion
- Worker de ingestion: ao classificar documento, tentar extrair entidades
- Ex: documento com `type: book_note` → criar entidade `book`
- Extração inicial via regras simples (frontmatter, filename)

## Critério de Aceitação
- [ ] CRUD de entities funcional via API
- [ ] CRUD de relations funcional via API
- [ ] CRUD de assets funcional via API
- [ ] Agente consegue buscar entidades e criar novas
- [ ] UniqueConstraints respeitados (sem duplicatas)
- [ ] Índices GIN em metadata funcionam

## Arquivos envolvidos
- **Criados:** `routers/entities.py`, `services/knowledge_graph.py`,
  `agents/tools/catalog_tools.py`
- **Alterados:** `app.py` (incluir rotas), `agents/graph.py` (registrar tools)
