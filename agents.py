import os
from dotenv import load_dotenv
from crewai import Agent
from crewai_tools import SerperDevTool
from tools import pdf_rag_tool

load_dotenv()

# Guardrail settings loaded from .env
max_rpm_setting = int(os.getenv("MAX_RPM", 10))
max_exec_time = int(os.getenv("MAX_EXECUTION_TIME", 120))
max_iterations = int(os.getenv("MAX_ITER", 3))

# Initialize Web Search Tool
web_search_tool = SerperDevTool()

# 1. HR Policy Assistant (RAG Agent)
hr_assistant_agent = Agent(
    role="IIA HR Policy Assistant",
    goal="Provide accurate and concise answers based on the IIA HR Policy document.",
    backstory="You are an internal HR policy expert specializing in Indian Industries Association policies.",
    tools=[pdf_rag_tool],
    max_rpm=max_rpm_setting,
    max_iter=max_iterations,
    max_execution_time=max_exec_time,
    verbose=True
)

# 2. Web Search Assistant
web_search_agent = Agent(
    role="Web Search Assistant",
    goal="Search the internet for accurate, up-to-date supplementary context related to user queries.",
    backstory="You are a skilled web research expert capable of gathering live information efficiently.",
    tools=[web_search_tool],
    max_rpm=max_rpm_setting,
    max_iter=max_iterations,
    max_execution_time=max_exec_time,
    verbose=True
)

# 3. Entry Agent (Google Sheets Logging Specialist)
entry_agent = Agent(
    role="Data Entry Specialist",
    goal="Compile the responses from the HR Assistant and Web Assistant into clean text.",
    backstory="You organize inputs cleanly and ensure accurate record-keeping.",
    max_rpm=max_rpm_setting,
    max_iter=max_iterations,
    max_execution_time=max_exec_time,
    verbose=True
)