import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

def append_to_sheet(query: str, assistant_response: str, web_response: str):
    """Appends the user query and both agent responses to Google Sheets."""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds_path = os.getenv("GOOGLE_SHEETS_CREDS_FILE", "google_credentials.json")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME", "CrewAI Output Logs")
    
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
        
        # Append row: Query, HR Assistant Response, Web Search Response
        sheet.append_row([query, assistant_response, web_response])
        return "Log successfully saved to Google Sheets."
    except Exception as e:
        return f"Failed to log to Google Sheets: {str(e)}"