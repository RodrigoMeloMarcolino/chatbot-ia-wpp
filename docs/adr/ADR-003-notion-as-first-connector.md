# ADR-003: Notion como primeiro connector de ingestão

## Status
Aceito.

## Contexto
O Second Brain precisa de fontes de conhecimento. O sistema original só
aceitava PDFs dropados em pasta. É necessário um conector programático
para um serviço real de conhecimento.

## Decisão
Implementar Notion API como primeiro conector de ingestão, em vez de
Obsidian, Google Drive ou filesystem.

## Consequências
**Positivas:**
- Notion é rico em estrutura (databases, páginas, metadados)
- API oficial bem documentada (`notion-client`)
- Conteúdo já organizado (diferente de filesystem cru)
- Valida o modelo de hierarquia (database → páginas → bloco)

**Negativas:**
- Depende de API externa (rate limits, mudanças de API)
- Requer criar integração Notion (passo extra de setup)
- Obsidian vault local é mais "self-hosted"

## Alternativas consideradas
- **Obsidian vault:** mais self-hosted, mas sem API oficial confiável
- **Google Drive:** viável, mas escopo maior
- **Filesystem:** simples demais, não valida modelo de fontes
