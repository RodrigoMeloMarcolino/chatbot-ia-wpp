# Tasks — Second Brain

Este diretório contém o plano de implementação dividido em 9 fases.

## Fases

| # | Nome | Tasks | Depende de |
|---|------|-------|------------|
| 1 | [Core Migration](01-core-migration.md) | 8 | — |
| 2 | [Hybrid RAG](02-hybrid-rag.md) | 6 | Fase 1 |
| 3 | [Ingestion Pipeline](03-ingestion-pipeline.md) | 5 | Fase 1 |
| 4 | [Notion Connector](04-notion-connector.md) | 4 | Fase 3 |
| 5 | [Agent Orchestrator](05-agent-orchestrator.md) | 5 | Fase 2, Fase 3 |
| 6 | [Conhecimento Estruturado](06-structured-knowledge.md) | 5 | Fase 5 |
| 7 | [Book Catalog](07-book-catalog.md) | 5 | Fase 6 |
| 8 | [Portfolio Polish](08-portfolio-polish.md) | 6 | Fase 1–7 |
| 9 | [Web UI](09-web-ui.md) | 6 | Fase 2, Fase 7 |

## Como usar

Cada arquivo de fase contém:

- **Objetivo:** o que a fase entrega
- **Tarefas:** checklist detalhado do que implementar
- **Critério de Aceitação:** o que precisa funcionar ao final
- **Arquivos envolvidos:** quais criar, alterar ou remover

Implemente uma fase por vez, validando o critério de aceitação antes
de passar para a próxima.
