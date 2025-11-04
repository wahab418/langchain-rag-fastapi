from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
load_dotenv()
def load_llm():
    print("we load a groq model")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=512
    )
    print("groq llm loaded successfully.")
    return llm
print("model.....")  