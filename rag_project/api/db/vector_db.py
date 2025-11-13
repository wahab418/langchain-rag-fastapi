from rag_project.api.utils.utils import text_splitter
from rag_project.api.embeddings.embeddings import embeddings
# from rag_project.api.embeddings.embeddings import embedding_model
from langchain_community.vectorstores import Chroma
import uuid
import os
import shutil

vector_store = Chroma(
    collection_name="example_collection",
    
    embedding_function=embeddings,
    
    persist_directory="./rag_project/api/db/chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

def store_vector_db(docs,workspace_id):
    splitted_docs = text_splitter(docs)
    persist_dir = f"./rag_project/api/db/chroma_langchain_db/workspace_{workspace_id}"
    os.makedirs(persist_dir, exist_ok=True)

    vector_store = Chroma(
        collection_name=f"workspace_{workspace_id}",
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )

    vector_store.add_documents(splitted_docs)
    vector_store.persist()
    return


def delete_vector_db(workspace_id):
    persist_dir = f"./rag_project/api/db/chroma_langchain_db/workspace_{workspace_id}"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
    return