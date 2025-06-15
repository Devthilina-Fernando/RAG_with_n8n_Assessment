from langchain.chains import RetrievalQA
from dependencies import vector_store, llm
from schemas.base import ErrorResponse

class LLMService:
    @staticmethod
    def get_qa_chain():
        try:
            return RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"LLM service initialization failed: {str(e)}"
            )