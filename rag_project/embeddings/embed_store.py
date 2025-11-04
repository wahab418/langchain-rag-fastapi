from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PATH = r"rag_project\data\processed"

def create_and_save_vectorstore(split_docs):
    print(" Creating embeddings and saving to Chroma...")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    vectorstore.persist()
    print(f" Vector store created and saved at {CHROMA_PATH}")
    return vectorstore


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    print("Loaded existing vector store.")
    return vectorstore
print("done........")
