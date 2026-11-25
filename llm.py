import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm(temperature=0.3):
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
    )

def ask_llm(prompt: str) -> str:   # planner.py keeps using this
    return get_llm().invoke(prompt).content