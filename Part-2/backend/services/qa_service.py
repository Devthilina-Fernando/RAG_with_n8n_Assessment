from services.llm_service import LLMService
from schemas.qa import QAResponse
from langchain.prompts import PromptTemplate

class QAService:
    def __init__(self):
        self.qa_prompt = PromptTemplate(
            template="""Answer the question using ONLY the provided context. Follow these rules:
            1. If the answer isn't in the context, say "I don't have information about that"
            2. Never invent details or use outside knowledge
            3. Keep answers concise and factual
            
            Context:
            {context}
            
            Question: {question}
            Answer:""",
            input_variables=["context", "question"]
        )
        
        base_chain = LLMService.get_qa_chain()
        
        self.qa_chain = base_chain.copy()
        self.qa_chain.combine_documents_chain.llm_chain.prompt = self.qa_prompt

    def ask_question(self, question: str) -> QAResponse:
        try:
            result = self.qa_chain({"query": question})
            
            sources = [
                {
                    "source": doc.metadata.get("source", "Unknown"),
                    "lines": f"{doc.metadata.get('loc.lines.from', '?')}-{doc.metadata.get('loc.lines.to', '?')}"
                }
                for doc in result['source_documents']
            ]
            
            return QAResponse(
                success=True,
                message="Successfully generated answer",
                data={
                    "answer": result['result'],
                    "sources": sources
                }
            )
        except Exception as e:
            return QAResponse(
                success=False,
                message=f"Error processing question: {str(e)}"
            )