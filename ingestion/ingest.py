from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pathlib import Path

load_dotenv()

def create_chunks(documents: list[Document]) -> list[Document]:
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
    if len(documents) == 0:
        raise ValueError("Documents are empty")

    for index, document in enumerate(documents):

        if not hasattr(document, "page_content"):
            raise AttributeError(f"Document at {index} has not a Attribute page_content.")

        if type(document.page_content) != str:
            raise TypeError(f"Document at {index} Attribute page_content is not a str. It is {type(document.page_content)}")
        
        if len(document.page_content.strip()) == 0:
            raise ValueError(f"Document content is empty. Index {index}")


    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    return splitter.split_documents(documents)


def create_embeddings(chunks:list[Document], path:str) -> Chroma:
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
    embedding = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2",  model_kwargs={"device": "cuda"})
    
    
    if len(path) == 0:
        raise ValueError("Given Path is empty.")
    
    if not Path(path).exists():
        raise ValueError(f"Path does not exists. Given Path: {path}")

    if len(chunks) == 0:
        raise ValueError("Chunks list is empty.")

    vector = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=path
    )
    
    return vector
