# Fase 4 — Notion Connector

## Objetivo
Conectar ao Notion API para sincronizar páginas e databases como
fontes de conhecimento do Second Brain.

## Tarefas

### 4.1 Setup de autenticação Notion
- Criar integração no Notion (https://www.notion.so/my-integrations)
- `NOTION_API_KEY` e `NOTION_DATABASE_IDS` no `.env`
- Instalar dependência: `notion-client`

### 4.2 Criar `ingestion/connectors/notion.py`
- `NotionConnector` class com métodos:
  - `list_pages(database_id)` — listar páginas de um database
  - `get_page_content(page_id)` — extrair texto + estrutura
  - `sync_database(database_id)` — sync completo de um database
- Tratamento de rate limiting (retry com backoff)
- Mapeamento de tipos Notion → tipos Second Brain:
  - `page` → `document`
  - `database` → `source`
  - `child_page` → documento filho (parent_id)
- Extrair `title`, `summary`, `created_time`, `last_edited_time`

### 4.3 Criar trigger de sync
- `POST /v1/ingestion/sources/notion` — trigger manual de sync
- Worker processa: cria/atualiza Source → lista páginas → cria
  ingestion_jobs para cada página nova ou alterada
- Dedup por `canonical_uri` (URL da página Notion)

### 4.4 Classificação de documentos do Notion
- Documentos do Notion são classificados por:
  - `properties.type` se existir no database
  - Título/heurística
  - Frontmatter-like em conteúdo

## Critério de Aceitação
- [ ] Notion connector autentica e lista páginas
- [ ] Sync de database cria documentos no Second Brain
- [ ] Conteúdo das páginas é indexado e consultável
- [ ] Re-sync não duplica documentos (idempotente)
- [ ] Rate limiting tratado

## Arquivos envolvidos
- **Criados:** `ingestion/connectors/notion.py`
- **Alterados:** `ingestion/api.py`, `core/config.py`, `requirements.txt`
