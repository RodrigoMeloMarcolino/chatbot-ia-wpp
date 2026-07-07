from datetime import date

from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from chains import get_rag_chain
from state import AgentState
from llms import get_llm_with_tools
from tools import TOOL_BY_NAME, TOOLS


rag_chain = get_rag_chain()
tool_calling_llm = get_llm_with_tools(TOOLS)


def log(*args):
    print('[GRAPH]', *args)

def get_last_user_input(messages):
    user_messages = [
        message for message in messages
        if isinstance(message, HumanMessage)
    ]

    return user_messages[-1].content

def prepare_turn(state: AgentState):
    return {
        'tool_messages': [],
        'tool_context': ''
    }

def decide_tools(state: AgentState):
    current_date = date.today().isoformat()
    decision_messages = [
        SystemMessage(
            content=(
                'Voce decide se precisa chamar ferramentas antes do RAG. '
                f'Data atual: {current_date}. '
                'Use duckduckgo_search quando a pergunta depender de informacao atual, '
                'noticias, datas, eventos, precos, versoes recentes ou fatos externos '
                'que podem ter mudado. Quando chamar a busca, escreva uma query objetiva '
                'e inclua o ano atual se a pergunta for sobre evento ou agenda atual. '
                'Se a pergunta for conversacional ou puder ser respondida apenas pelo historico/RAG, '
                'nao chame ferramenta.'
            )
        ),
        *state['messages']
    ]

    response = tool_calling_llm.invoke(decision_messages)
    tool_calls = getattr(response, 'tool_calls', None) or []

    if tool_calls:
        log('tools_decided', [tool_call['name'] for tool_call in tool_calls])
    else:
        log('no_tools_decided')

    return {
        'tool_messages': [response]
    }

def route_after_tool_decision(state: AgentState):
    tool_messages = state['tool_messages']

    if not tool_messages:
        return 'rag'
    
    last_message = tool_messages[-1]

    if getattr(last_message, 'tool_calls', None):
        return 'execute_tools'
    
    return 'rag'

def execute_tools(state: AgentState):
    tool_messages = state.get('tool_messages', [])
    last_message = tool_messages[-1]

    new_tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        tool_call_id = tool_call['id']

        tool = TOOL_BY_NAME[tool_name]
        log('tool_start', tool_name, tool_args)
        result = tool.invoke(tool_args)
        log('tool_done', tool_name, str(result)[:300])

        new_tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call_id,
                name=tool_name
            )
        )

    return {
        'tool_messages': tool_messages + new_tool_messages
    }

def collect_tool_context(state: AgentState):
    tool_results = [
        message.content
        for message in state.get('tool_messages', [])
        if isinstance(message, ToolMessage)
    ]

    tool_context = '\n\n'.join(tool_results)
    log('tool_context_chars', len(tool_context))

    return {
        'tool_context': tool_context
    }

def call_rag(state: AgentState):
    messages = state['messages']
    user_input = get_last_user_input(messages)

    answer = rag_chain.invoke({
        'input': user_input,
        'chat_history': messages[:-1],
        'tool_context': state.get('tool_context', '')
    })
    log('rag_answer_chars', len(answer))

    return {
        'messages': [AIMessage(content=answer)]
    }
