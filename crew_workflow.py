import os
from crewai import Task, Crew, Process
from agents import hr_assistant_agent, web_search_agent, entry_agent
from sheets_helper import append_to_sheet

def run_hr_crew(user_query: str):
    """Executes the 3-agent pipeline and records the output in Google Sheets."""
    
    # Task 1: Search IIA HR Policy Document
    hr_task = Task(
        description=f"Search the IIA HR Policy document and answer the user query: '{user_query}'",
        expected_output="A detailed answer based solely on the IIA HR Policy PDF.",
        agent=hr_assistant_agent
    )
    
    # Task 2: Perform Web Search
    web_task = Task(
        description=f"Search the web for supplementary context regarding: '{user_query}'",
        expected_output="A summary of current internet search findings related to the user's question.",
        agent=web_search_agent
    )
    
    # Task 3: Entry Agent Formatting
    entry_task = Task(
        description="Review the answers from the HR Policy Assistant and Web Search Assistant. Format them clearly.",
        expected_output="A cleanly formatted summary containing both responses.",
        agent=entry_agent
    )
    
    # Assemble Crew
    crew = Crew(
        agents=[hr_assistant_agent, web_search_agent, entry_agent],
        tasks=[hr_task, web_task, entry_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute execution flow
    crew.kickoff()
    
    # Extract responses directly from task execution results
    hr_response = str(hr_task.output.raw) if hr_task.output else "No response."
    web_response = str(web_task.output.raw) if web_task.output else "No response."
    
    # Log results to Google Sheets
    sheet_status = append_to_sheet(
        query=user_query,
        assistant_response=hr_response,
        web_response=web_response
    )
    
    return {
        "hr_response": hr_response,
        "web_response": web_response,
        "sheet_status": sheet_status
    }