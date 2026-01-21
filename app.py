import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from github_client import parse_repo_url, get_issue_details
from llm_service import analyze_issue

# Load environment variables (for OPENAI_API_KEY)
load_dotenv()

app = Flask(__name__)

# Custom filter for pretty printing JSON in templates 
@app.template_filter('pretty_json')
def pretty_json(value):
    return json.dumps(value, indent=2)  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # 1. INPUT VALIDATION
    repo_url = request.form.get('repo_url', '').strip()
    issue_number = request.form.get('issue_number', '').strip()

    # Reject empty fields
    if not repo_url:
        return render_template('index.html', error="Please provide a Repository URL.")
    
    if not issue_number:
        return render_template('index.html', error="Please provide an Issue Number.")

    # Reject non-integer issue number
    if not issue_number.isdigit():
        return render_template('index.html', error="Issue Number must be a valid integer.")

    try:
        # 2. GITHUB API ERROR HANDLING
        parsed_url = parse_repo_url(repo_url)
        if not parsed_url:
             return render_template('index.html', error="Invalid GitHub URL. Expected format: https://github.com/owner/repo")

        # Fetch data from GitHub (handle network/API errors)
        try:
            issue_data = get_issue_details(parsed_url['owner'], parsed_url['repo'], int(issue_number))
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                return render_template('index.html', error=f"Issue #{issue_number} not found in {parsed_url['owner']}/{parsed_url['repo']}. Check if the repository is private or the issue number is incorrect.")
            elif "403" in error_msg:
                return render_template('index.html', error="GitHub API rate limit exceeded. Please try again later.")
            else:
                raise e # Re-raise to catch in outer block
        
        # Handle issues with no content
        if not issue_data.get('title') and not issue_data.get('body'):
            return render_template('index.html', error="The specified issue seems to be empty or inaccessible.")

        # 3. AI SERVICE ERROR HANDLING
        # Check for API Key presence
        if not os.environ.get("OPENAI_API_KEY"):
            return render_template('index.html', error="System Configuration Error: OPENAI_API_KEY is missing.")

        # Analyze with AI
        try:
            analysis_result = analyze_issue(issue_data)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg: # OpenAI Rate Limit
                 return render_template('index.html', error="AI Service is currently busy (Quota Exceeded). Please try again later.")
            raise e

        # Render the result page with the analysis data
        return render_template('result.html', result=analysis_result)

    except Exception as e:
        # Catch-all for any other unexpected errors
        print(f"Error processing request: {e}")
        # Show a clean message to the user, log the stack trace server-side
        return render_template('index.html', error=f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
 