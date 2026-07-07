from langchain_openai import ChatOpenAI

from core.config import OPENAI_MODEL_NAME, OPENAI_MODEL_TEMPERATURE


def get_default_llm():
    return ChatOpenAI(
        model=OPENAI_MODEL_NAME,
        temperature=OPENAI_MODEL_TEMPERATURE
    )

def get_llm_with_tools(tools):
    return get_default_llm().bind_tools(tools)