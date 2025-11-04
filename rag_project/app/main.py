from rag_project.loaders.pdf_loader import  load_pdfs_from_folder
from rag_project.utils.text_splitter import split_documents
from rag_project.embeddings.embed_store import create_and_save_vectorstore
from rag_project.llm.llm_model import load_llm
from rag_project.retrival.retriever import get_retriever

def main():
    #load
    folder_path = r"rag_project\data\raw"
    docs = load_pdfs_from_folder(folder_path)
    #split
    split_docs = split_documents(docs)
    print(f"process completed: {len(split_docs)}")
    
    #vecrtor store
    vectorstore = create_and_save_vectorstore(split_docs)

    llm = load_llm()
    retriever = get_retriever()

    query = "give me the information about the images in files"

    relevant_docs = retriever.invoke(query)
    print(f"retrieved {len(relevant_docs)} relevent chunks")
    
    #custom prompt
    context = "\n".join([doc.page_content for doc in relevant_docs])
    prompt = f""" You are a helpful assistant. Use the context below to answer the question.Context:{context},Question:{query} Answer:"""
    
    response = llm.invoke(prompt)
    
    print("the answer is ", response.content)
    
   
    
if __name__ == "__main__":
    main()
    print("mainn..........")