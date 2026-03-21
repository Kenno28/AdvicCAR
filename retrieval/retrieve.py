from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embedding = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2", model_kwargs={"device": "cuda"})


def retrieve(query:str):
    db = Chroma(
        persist_directory="C:/Users/Eray/Desktop/Projekt/AdviCAR/db",
        embedding_function=embedding,
    )

    return db.similarity_search(query, k=10)