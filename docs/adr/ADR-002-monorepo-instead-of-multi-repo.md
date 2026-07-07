# ADR-002: Monorepo em vez de multi-repositório

## Status
Aceito.

## Contexto
O livedoc original propõe 8 repositórios separados (rag-api, ingestion-api,
agent-orchestrator, web-ui, infra, docs, book-catalog). Na prática, como
desenvolvedor solo, o overhead de múltiplos repositórios supera os benefícios.

## Decisão
Manter tudo em um único repositório (`chatbot-ia-wpp/`) com separação lógica
em diretórios (`core/`, `rag/`, `ingestion/`, `agents/`, `modules/`, `ui/`).

## Consequências
**Positivas:**
- Código compartilhado sem publish de pacotes
- Refatorações cross-module num commit só
- CI/CD unificado
- Deploy único (um docker-compose)
- Desenvolvimento local mais simples

**Negativas:**
- Limite de scaling (um repositório grande)
- Acoplamento implícito possível
- Difícil extrair componentes no futuro

## Alternativas consideradas
- **Multi-repo completo:** 8 repositórios para dev solo = overhead alto
- **Monorepo com pacotes Python:** complexidade adicional sem ganho real pro MVP
