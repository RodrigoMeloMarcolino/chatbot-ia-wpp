from langgraph.graph import StateGraph, START, END

from nodes import (
    call_rag,
    collect_tool_context,
    decide_tools,
    execute_tools,
    prepare_turn,
    route_after_tool_decision,
)
from state import AgentState


def build_graph(checkpointer):
    builder = StateGraph(AgentState)

    builder.add_node('prepare_turn', prepare_turn)
    builder.add_node('decide_tools', decide_tools)
    builder.add_node('execute_tools', execute_tools)
    builder.add_node('collect_tool_context', collect_tool_context)
    builder.add_node('rag', call_rag)

    builder.add_edge(START, 'prepare_turn')
    builder.add_edge('prepare_turn', 'decide_tools')

    builder.add_conditional_edges(
        'decide_tools',
        route_after_tool_decision,
        {
            'execute_tools': 'execute_tools',
            'rag': 'rag'
        }
    )

    builder.add_edge('execute_tools', 'collect_tool_context')
    builder.add_edge('collect_tool_context', 'rag')
    builder.add_edge('rag', END)

    return builder.compile(checkpointer=checkpointer)