import os
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv

load_dotenv()

# Define path to the uploaded PDF
PDF_PATH = os.getenv("PDF_PATH", "IIA HR Policy.pdf")

# Initialize the PDF RAG Search Tool using CrewAI tools
try:
    pdf_rag_tool = PDFSearchTool(
        pdf=PDF_PATH,
        config=dict(
            llm=dict(
                provider=os.getenv("CHAT_PROVIDER"),
                config=dict(
                    model=os.getenv("CHAT_MODEL"),
                ),
            ),
            embedder=dict(
                provider=os.getenv("CHAT_PROVIDER"),
                config=dict(
                    model=os.getenv("EMBED_MODEL"),
                ),
            ),
        )
    )
except Exception as e:
    print(f"Unable to search using PDF Rag Tool : {e}")