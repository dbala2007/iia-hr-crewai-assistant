# IIA HR CrewAI

A Streamlit-based multi-agent application that answers HR policy questions using a local PDF policy document and live web search results. The app combines CrewAI agents, Google Sheets logging, and a protected login screen for internal use.

## Overview

This project allows users to ask questions such as leave policy, probation, attendance, benefits, or compliance related matters. The application:

- searches the internal HR policy PDF for grounded answers
- fetches supplementary web context for current information
- combines both responses into a clear result for the user
- logs queries and answers to a Google Sheet
- exposes the app through a lightweight Streamlit interface

## Project Structure

- `app.py` — Streamlit UI and access gate
- `crew_workflow.py` — orchestrates the CrewAI workflow
- `agents.py` — defines the HR, web-search, and formatting agents
- `tools.py` — configures the PDF search tool
- `sheets_helper.py` — appends query and response data to Google Sheets
- `requirements.txt` — Python dependencies
- `.env.example` — sample environment variables
- `google_credentials.json.example` — sample Google service account credential format
- `Dockerfile` — container build definition
- `docker-compose.yml` — container run configuration
- `.gitignore` — excludes local/private config and virtual environment files

## Features

- Secure Streamlit login using `APP_PASSWORD`
- CrewAI multi-agent workflow
- PDF-based RAG for internal HR policy answers
- Live web search via Serper Dev
- Google Sheets audit logging
- Docker support for deployable container setup

## Prerequisites

Before running the app, make sure you have:

- Python 3.11+
- pip
- A valid OpenAI API key
- A Serper API key
- A Google service account JSON credential for Sheets access
- The HR policy PDF file available locally

## Local Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

4. Copy the environment example file and configure secrets:

```bash
copy .env.example .env
```

Update `.env` with your values:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
APP_PASSWORD=your_secure_streamlit_password
MAX_RPM=10
MAX_EXECUTION_TIME=120
MAX_ITER=3
GOOGLE_SHEETS_CREDS_FILE=google_credentials.json
GOOGLE_SHEET_NAME=your-google-sheets-name
PDF_PATH=IIA HR Policy.pdf
CHAT_PROVIDER="openai"
CHAT_MODEL="gpt-4o-mini"
EMBED_MODEL="text-embedding-3-small"
```

5. Add your Google service account credentials file:

- place `google_credentials.json` in the project root
- ensure the JSON file corresponds to a service account with access to the target Google Sheet

6. Place the HR policy PDF in the project root and ensure the filename matches `PDF_PATH`.

> Important: do not commit sensitive credentials or the policy PDF to Git. Keep them local or manage them via a secure environment secret store.

## Run the App

### Option 1: Local Python

```bash
streamlit run app.py
```

### Option 2: Docker Compose

```bash
docker-compose up --build
```

The app runs on port `8502` by default.

## Docker

The included `Dockerfile` installs Python dependencies and launches the Streamlit application on port `8502`.

Example:

```bash
docker build -t iiahrcrew-app .
docker run -p 8502:8502 --env-file .env iiahrcrew-app
```

## GitLab Push Instructions

### 1. Initialize Git repository

```bash
git init
```

### 2. Add files

```bash
git add .
```

### 3. Commit changes

```bash
git commit -m "Initial commit for IIA HR CrewAI app"
```

### 4. Create a GitLab repository

In GitLab, create a new empty project and copy the remote URL.

### 5. Add the GitLab remote

```bash
git remote add origin git@gitlab.com:YOUR_USERNAME/YOUR_PROJECT.git
```

### 6. Push to GitLab

```bash
git branch -M main
git push -u origin main
```

## Recommended Git Ignore

The repository already includes a `.gitignore` file for local-only items such as:

- `.venv/`
- `__pycache__/`
- `google_credentials.json`
- environment files like `.env`

Keep these out of version control.

## Notes

- The app is designed for internal organizational use and uses a password gate.
- Google Sheets logging is optional and depends on valid credentials and spreadsheet access.
- The PDF-based policy lookup is the source of truth for HR answers; the web search is supplementary context.

## License

This project is intended for internal use. Add an appropriate license if you plan to share the repository externally.
