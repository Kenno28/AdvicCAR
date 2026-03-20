import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

load_dotenv()

def create_chunks(documents):
    """
    Splits a list of documents into smaller overlapping text chunks.

    This function uses a RecursiveCharacterTextSplitter to divide
    input documents into chunks of fixed size with overlap,
    which is useful for downstream tasks like embedding or retrieval.

    Args:
        documents (list): A list of documents (e.g., LangChain Document objects)
                          to be split into smaller chunks.

    Returns:
        list: A list of chunked document objects.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    return splitter.split_documents(documents)

def create_embeddings(chunks, path:str):
    """
    Creates vector embeddings from text chunks and stores them in a persistent vector database.

    This function uses a HuggingFace embedding model to convert text chunks
    into vector representations and stores them in a Chroma vector store.
    If no valid path is provided, it falls back to the SAVE_PATH environment variable.

    Args:
        chunks (list): A list of document chunks (e.g., LangChain Document objects)
                    to be embedded.
        path (str): Directory path where the vector database will be persisted.

    Raises:
        Exception: If no valid path is provided and SAVE_PATH is not set.

    Returns:
        Chroma: The created and persisted Chroma vector store instance.
    """
    embedding = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

    if not Path(path).exists():
        os_path =  os.getenv("SAVE_PATH")
        if not os_path:
            raise ValueError("No valid Path")
        else:
            path = os_path

    vector = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=path
    )
    
    return vector
