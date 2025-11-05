import os
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdfs_from_folder(folder_path: str):
    
    
    all_docs = []
    
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Loading: {file_name}")
            loader = PyMuPDFLoader(file_path)
            docs = loader.load()
            all_docs.extend(docs)
            
    print(" All PDFs loaded successfully......")
    return all_docs
