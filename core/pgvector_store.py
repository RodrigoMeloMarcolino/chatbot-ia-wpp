from typing import Optional

from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from core.config import (
    DATABASE_URL,
    PGVECTOR_COLLECTION_NAME
)


SYNCHRONOUS_DATABASE_URL = DATABASE_URL.replace('+asyncpg', '')

_vectorstore: Optional[PGVector] = None

def get_vectorstore() -> PGVector:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = PGVector(
            embeddings=OpenAIEmbeddings(),
            collection_name=PGVECTOR_COLLECTION_NAME,
            connection=SYNCHRONOUS_DATABASE_URL,
        )
    return _vectorstore
