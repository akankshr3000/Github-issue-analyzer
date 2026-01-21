# AI-Powered GitHub Issue Analyzer

An AI-powered web application that analyzes GitHub issues and generates a structured JSON summary including issue type, priority score, suggested labels, and potential impact.  
The project helps developers and maintainers quickly understand and triage GitHub issues.

---
 
## 🚀 Features

- AI-driven GitHub issue analysis using OpenAI GPT
- Fetches real-time issue data from public GitHub repositories
- Strict JSON output suitable for automation and reporting
- Robust input validation and error handling
- Clean and minimal UI for fast usability
- Secure API key handling via environment variables

---

##  System Design Overview

- **app.py**  
  Acts as the main Flask server and orchestrates the workflow.

- **github_client.py**  
  Fetches issue title, body, and comments using the GitHub REST API.

- **llm_service.py**  
  Handles prompt engineering and communication with the OpenAI API.

This separation of concerns ensures a clean, logical, and maintainable system design.

---

## Edge Cases Handled

The application gracefully handles the following scenarios:
- Empty repository URL
- Invalid GitHub repository URL
- Private GitHub repositories
- Non-existent issue numbers
- Issues with no comments
- Issues with empty descriptions
- Very long issue bodies or large comment threads

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **AI Model:** OpenAI GPT (direct API call)
- **External API:** GitHub REST API
- **Frontend:** HTML + CSS (Jinja templates)
- **Dependency Management:** requirements.txt

---

##  Setup & Run (Under 5 Minutes)

### 1️ Prerequisites
- Python 3.9 or higher
- Internet connection
- OpenAI API Key

---

### 2️ Installation

Clone the repository and navigate into the project directory:

```bash
git clone <repository_url>
cd githubproj
```

(Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 3️ OpenAI API Key Configuration (Mandatory)

For security reasons, the OpenAI API key is not included in the project.

Create an API key from:
https://platform.openai.com/account/api-keys

Set the API key as an environment variable:

**Windows (PowerShell):**
```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

**macOS / Linux:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

Restart the terminal after setting the environment variable.

---

### 4️ Run the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

##  Usage

1. Enter a public GitHub repository URL  
2. Enter a valid issue number  
3. Click **Analyze Issue**  
4. View the AI-generated structured JSON analysis

---

##  Sample Output

```json
{
  "summary": "User reports a crash related to hook execution order.",
  "type": "bug",
  "priority_score": "4 – High impact on developer experience",
  "suggested_labels": ["bug", "hooks", "react"],
  "potential_impact": "May cause unexpected crashes during development."
}
```

---

##  Security Notes

- No API keys are stored in the repository
- All secrets are handled using environment variables
- Safe for public GitHub submission

---

##  Design Decision

Direct OpenAI API calls are used instead of higher-level abstraction libraries to keep the system minimal, transparent, and fast.

---
