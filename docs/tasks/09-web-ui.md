# Fase 9 — Web UI (Streamlit)

## Objetivo
Criar uma interface web para o Second Brain com chat, dashboards
de ingestion, visualização de fontes e custos.

## Tarefas

### 9.1 Setup do Streamlit
- Criar `ui/app.py` como entrypoint
- `requirements.txt`: adicionar `streamlit`
- Docker: service separado ou integrado ao bot (decidir)
- Config via variáveis de ambiente (`API_BASE_URL`)

### 9.2 Chat/Query Interface
- Input de texto com envio
- Histórico de conversa (session_state)
- Resposta com markdown renderizado
- Fontes/citações em expander abaixo da resposta
- Indicador de carregamento durante chamada ao `/v1/ask`
- Seleção de filtros (source, document_type) na sidebar

### 9.3 Painel de Ingestion Jobs
- Lista de jobs com status, tipo, data, erros
- Filtros: status, source, data range
- Upload de documento via drag-and-drop
- Status em tempo real (polling a cada 5s)

### 9.4 Visualização de Chunks e Fontes
- Input de search → `/v1/search` → resultados
- Chunks exibidos com: conteúdo, score, documento de origem
- Link para documento original (se URI existir)
- Metadata filter sidebar

### 9.5 Dashboard de Custos
- Gráfico de tokens por dia/semana/mês
- Custo estimado por modelo
- Total de requisições (RAG vs. embedding vs. LLM)
- Fonte dos dados: logs ou tabela de custos

### 9.6 Book Catalog View
- Tabela de livros catalogados
- Busca por título, autor, status
- Detalhe do livro: assets, notas relacionadas, metadados
- Botão para forçar extração de livro de documento

## Critério de Aceitação
- [ ] Chat funcional com markdown e fontes
- [ ] Upload de documento via UI
- [ ] Status de ingestion jobs visível
- [ ] Search de chunks funcional
- [ ] Dashboard de custos com dados reais
- [ ] Book catalog view funcional

## Arquivos envolvidos
- **Criados:** `ui/app.py`, `ui/pages/`, `ui/components/`
- **Alterados:** `docker-compose.yaml` (se UI for serviço separado),
  `requirements.txt`
