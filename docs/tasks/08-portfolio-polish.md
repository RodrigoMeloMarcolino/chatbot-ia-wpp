# Fase 8 — Portfolio Polish

## Objetivo
Elevar a qualidade do projeto para padrão de portfólio profissional:
testes, type hints, lint, documentação e CI/CD impecáveis.

## Tarefas

### 8.1 README.md
- Título e descrição do projeto
- Stack tecnológica
- Arquitetura (diagrama simples em ASCII ou Mermaid)
- Pré-requisitos (Docker, Python 3.13, uv)
- Setup local passo a passo
- Comandos de desenvolvimento (lint, test, typecheck)
- Estrutura de diretórios comentada
- Screenshots (quando UI existir)

### 8.2 Testes
- `tests/unit/`: testes unitários para:
  - `core/models.py` (fábricas, validações)
  - `rag/hybrid_retriever.py` (mock do vector store)
  - `ingestion/classifier.py` (classificação por tipo)
  - `agents/nodes.py` (fluxo do LangGraph)
  - `modules/books/extractor.py` (extração de livros)
- `tests/integration/`: testes de integração com Docker:
  - Fluxo completo: upload → ingestion → RAG query
  - API contracts (/v1/ask, /v1/search)
  - Webhook WhatsApp (mock do Evolution API)
- Configuração pytest: `pyproject.toml` ou `pytest.ini`
- Fixtures reutilizáveis, factories para models
- Cobertura mínima: > 70%

### 8.3 Type hints e mypy
- Projeto 100% type-annotated (exceto testes onde inferência é suficiente)
- `mypy` configurado com `--strict` parcial
- `pyproject.toml` com configuração mypy
- `make typecheck` no Makefile

### 8.4 Lint e formatação
- Ruff configurado (já usado no Moira, mesma config)
- `make lint` + `make format`
- CI (GitHub Actions) rodando em todo PR:
  - lint
  - typecheck
  - unit tests
  - build Docker image

### 8.5 Makefile
- `make install` — uv sync
- `make lint` — ruff check
- `make format` — ruff format
- `make typecheck` — mypy
- `make test` — pytest
- `make test-unit` — pytest -m "not integration"
- `make test-integration` — docker compose + pytest -m integration
- `make docker-build` — docker build
- `make up` — docker compose up -d
- `make down` — docker compose down

### 8.6 ADRs
- Documentar decisões de arquitetura em `docs/adr/`

## Critério de Aceitação
- [ ] `make lint` passa sem erros
- [ ] `make typecheck` passa sem erros
- [ ] `make test-unit` passa com cobertura > 70%
- [ ] README.md completo e funcional
- [ ] GitHub Actions configurado e verde
- [ ] Makefile com todos os comandos

## Arquivos envolvidos
- **Criados:** `README.md`, `Makefile`, `.github/workflows/ci.yml`,
  `tests/unit/`, `tests/integration/`, `docs/adr/`
- **Alterados:** `pyproject.toml` (se existir)
