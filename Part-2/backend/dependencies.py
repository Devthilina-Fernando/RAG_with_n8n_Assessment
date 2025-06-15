from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone
from utils.config import get_settings

try:
    settings = get_settings()
    
    if not all([settings.pinecone_api_key, settings.openai_api_key, settings.pinecone_index_name]):
        raise ValueError("Missing required environment variables")

    pc = Pinecone(api_key=settings.pinecone_api_key)
    index = pc.Index(settings.pinecone_index_name)

    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.openai_api_key,
        model="text-embedding-ada-002"
    )

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        text_key="text"
    )

    llm = ChatOpenAI(
        openai_api_key=settings.openai_api_key,
        model="gpt-3.5-turbo",
        temperature=0.3
    )

except Exception as e:
    raise RuntimeError(f"Failed to initialize dependencies: {str(e)}")