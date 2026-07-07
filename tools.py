from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

duckduckgo_search = DuckDuckGoSearchResults(
    name='duckduckgo_search',
    description=(
        "Busca informações atuais na internet. Use quando a pergunta depender "
        "de dados recentes, notícias, versões atuais, preços ou informações externas."
    ),
    api_wrapper=DuckDuckGoSearchAPIWrapper(
        backend='lite'
    ),
)

TOOLS = [duckduckgo_search]
TOOL_BY_NAME = {tool.name: tool for tool in TOOLS}