from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()

client = Groq(api_key=os.getenv("GROP_API_KEY"))


def call_llm(messages, tools):
    if not os.getenv("MODEL_NAME"):
        raise ValueError("MODEL_NAME environment variable is not set.")

    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=messages,
        tools=tools,
        max_tokens=2000)
    
    return response