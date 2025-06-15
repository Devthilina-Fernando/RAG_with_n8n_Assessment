from dependencies import vector_store, llm
from schemas.summary import SummaryResponse

class SummaryService:
    @staticmethod
    def generate_summary(file_name: str) -> SummaryResponse:
        try:
            chunks = vector_store.similarity_search(
                query="",
                filter={"file_name": file_name},
                k=1000
            )
            
            if not chunks:
                return SummaryResponse(
                    success=False,
                    message="Document not found or has no content"
                )
            
            combined_text = "\n\n".join([doc.page_content for doc in chunks])
            truncated_text = combined_text[:15000]
            
            prompt = f"""
            You are a document summarization agent.

            Given a specific user query and a document's content, generate a focused and concise summary that addresses the query. Highlight the most relevant information, such as key points, decisions, or action items, based on the query.

            Do not include any information that is not explicitly present in the document.

            Document Content:
            {truncated_text}
            """

            
            response = llm.invoke(prompt)
            return SummaryResponse(
                success=True,
                message="Summary generated successfully",
                data={"summary": response.content.strip()}
            )
        except Exception as e:
            return SummaryResponse(
                success=False,
                message=f"Error generating summary: {str(e)}"
            )