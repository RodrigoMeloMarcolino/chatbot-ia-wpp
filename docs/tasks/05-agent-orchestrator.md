# Fase 5 — Agent Orchestrator

## Objetivo
Transformar o LangGraph atual em um orquestrador de agentes que
opera o Second Brain através de tools/APIs, em vez de chamar chains
diretamente.

## Tarefas

### 5.1 Criar `agents/tools/rag_tools.py`
- `ask_rag(question, filters, top_k)` → chama `POST /v1/ask`
  (ou chama service diretamente se estiver no mesmo processo)
- `search_documents(query, filters, top_k)` → chama `POST /v1/search`
- Ferramentas expostas como LangChain Tool com descrição clara

### 5.2 Criar `agents/tools/ingestion_tools.py`
- `trigger_ingestion(file_path, source_id, metadata)` → cria ingestion job
- `get_ingestion_job_status(job_id)` → retorna status atual
- `list_sources()` → lista fontes configuradas
- Ferramentas expostas como LangChain Tool

### 5.3 Refatorar `agents/graph.py`
- Manter estrutura LangGraph, mas nodes chamam tools acima
- Estado agora inclui:
  - `intent` qualificado (pergunta RAG, comando ingestão, consulta catálogo)
  - `tool_results` estruturados (não só strings)
- Nó `decide_tools` agora escolhe entre: RAG, ingestão, catálogo, web search
- Nó `call_rag` usa `ask_rag` tool em vez de chain direta

### 5.4 Refatorar `agents/nodes.py`
- `prepare_turn` — igual, reseta estado
- `decide_tools` — LLM decide entre ferramentas do Second Brain
  + DuckDuckGo (mantido do original)
- `execute_tools` — executa tools e guarda resultados estruturados
- `call_rag` — agora usa RAG tool (pode ser RAG puro ou com contexto de tools)
- Remover dependência direta de `rag/` (agente agora passa pelo orchestrator)

### 5.5 Atualizar `agents/state.py`
- Adicionar campos: `intent`, `tool_results` estruturados,
  `rag_context` (para enriquecer com tool context)

## Critério de Aceitação
- [ ] Agente WhatsApp consegue responder perguntas via RAG tool
- [ ] Agente WhatsApp consegue triggerar ingestão de documento
- [ ] Agente consulta status de ingestion jobs
- [ ] DuckDuckGo search continua funcionando para informações atuais
- [ ] Histórico de conversa mantido (LangGraph checkpointing)

## Arquivos envolvidos
- **Criados:** `agents/tools/rag_tools.py`, `agents/tools/ingestion_tools.py`
- **Alterados:** `agents/graph.py`, `agents/nodes.py`, `agents/state.py`,
  `agents/tools.py` (remover ou migrar)
