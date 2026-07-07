from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableSerializable

from prompts import contextualize_prompt, qa_prompt
from core.pgvector_store import get_vectorstore
from llms import get_default_llm


def _get_search_query(
        inputs: dict,
        contextualize_question_chain: RunnableSerializable[dict[str, Any], str]
    ) -> str:
    if inputs.get('chat_history'):
        return contextualize_question_chain.invoke(inputs)

    return inputs['input']

def get_rag_chain():
    llm = get_default_llm()
    retriever = get_vectorstore().as_retriever()

    contextualize_question_chain = (
        contextualize_prompt
        | llm
        | StrOutputParser()
    )
    retrieval_chain = (
        RunnableLambda(
            lambda inputs: _get_search_query(inputs, contextualize_question_chain)
        )
        | retriever
    )
    answer_chain = (
        qa_prompt
        | llm
        | StrOutputParser()
    )

    return (
        RunnablePassthrough.assign(
            context=retrieval_chain
        )
        | answer_chain
    )