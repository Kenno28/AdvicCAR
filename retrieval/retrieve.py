from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pathlib import Path


def retrieve(query:str, path:str, k:int=1) -> list[Document]:
    """
    Retrieves the top-k most relevant documents from a persisted Chroma vector database
    based on a similarity search.

    The function validates the query and database path, then performs a semantic search
    using the provided embedding function.

    Args:
        query (str): The search query used to retrieve relevant documents.
        path (Path): Path to the persisted Chroma database directory.
        k (int, optional): Number of top similar documents to return. Defaults to 1.

    Raises:
        NotADirectoryError: If the provided database path does not exist.
        ValueError: If the query is empty or contains only whitespace.

    Returns:
        list[Document]: A list of the top-k most relevant documents retrieved
        from the vector database.
    """
    if len(path) == 0:
        raise ValueError("No path given")
    
    if not Path(path).exists():
        raise NotADirectoryError("Database not found.")

    if len(query.strip()) == 0:
        raise ValueError("Query is empty")
    
    if k <= 0:
        raise ValueError("K can´t be less than 1")
    
    embedding = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2", model_kwargs={"device": "cuda"})

    db = Chroma(
        persist_directory=path,
        embedding_function=embedding,
    )

    return db.similarity_search(query, k=k)
