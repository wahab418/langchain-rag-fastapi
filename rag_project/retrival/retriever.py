from rag_project.embeddings.embed_store import load_vectorstore


def get_retriever():
    print('loading retriever from chroma vectorstore')
    
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={'k':2})
    
    print('retriever loaded successfully.')
    return retriever

print("retrieved.....")