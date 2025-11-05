from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(docs):
    """Split documents into smaller chunks for embeddings or RAG."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   
        chunk_overlap=200, 
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    split_docs = splitter.split_documents(docs)
    print(f" Split into {len(split_docs)} chunks.")
    return split_docs
print("splitted.....")