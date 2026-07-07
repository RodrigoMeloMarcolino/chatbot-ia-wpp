import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.pgvector_store import get_vectorstore
from core.config import (
    RAG_FILES_DIR
)


def _load_documents():
    docs = []
    processed_dir = os.path.join(RAG_FILES_DIR, 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    files = [
        os.path.join(RAG_FILES_DIR, f)
        for f in os.listdir(RAG_FILES_DIR)
        if f.endswith('.pdf')
    ]

    for file in files:
        loader = PyPDFLoader(file)
        docs.extend(loader.load())
        dest_path = os.path.join(processed_dir, os.path.basename(file))
        shutil.move(file, dest_path)

    return docs

def seed_vectorstore():
    processed_dir = os.path.join(RAG_FILES_DIR, 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    files = [
        os.path.join(RAG_FILES_DIR, f)
        for f in os.listdir(RAG_FILES_DIR)
        if f.endswith('.pdf')
    ]

    if not files:
        print(f'Nenhum PDF em {RAG_FILES_DIR}')
    
    print(f'Processando {len(files)} PDF(s)...')

    vs = get_vectorstore()
    total_chunks = 0

    for file in files:
        print(f'  📄 {os.path.basename(file)}')
        loader = PyPDFLoader(file)
        docs = loader.load()
        print(f'    Páginas: {len(docs)}')

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        vs.add_documents(splits)
        total_chunks += len(splits)

        dest_path = os.path.join(processed_dir, os.path.basename(file))
        shutil.move(file, dest_path)
        print(f"     ✅ Movido para processed/")

    print(f"\nConcluído. {total_chunks} chunk(s) inserido(s).")


if __name__ == '__main__':
    seed_vectorstore()