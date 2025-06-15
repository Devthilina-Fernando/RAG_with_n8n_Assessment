import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME")

def get_settings():
    return Settings()