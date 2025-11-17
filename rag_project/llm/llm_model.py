from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()
def load_llm():
    print("we load a groq model")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,     # deterministic output
        max_tokens=1024,   # safer for long JSON outputs
        tools=[], 
        tool_choice="none" # disable function/tool calling
    )
    print("groq llm loaded successfully.")
    return llm
print("model.....")  