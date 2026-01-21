import os
import json
import sys
from dotenv import load_dotenv
from github_client import parse_repo_url, get_issue_details
from llm_service import analyze_issue

# Load environment variables
load_dotenv()

def main():
    print("AI-Powered GitHub Issue Analyzer (CLI Mode)")
    print("-------------------------------------------")

    repo_url = input("Enter GitHub Repository URL: ").strip()
    if not repo_url:
        print("Error: Repository URL is required.")
        return

    issue_number_str = input("Enter Issue Number: ").strip()
    if not issue_number_str:
        print("Error: Issue Number is required.")
        return

    try:
        parsed_url = parse_repo_url(repo_url)
        if not parsed_url:
            print("Error: Invalid GitHub URL. Please use format https://github.com/owner/repo")
            return

        print(f"\nFetching issue #{issue_number_str} from {parsed_url['owner']}/{parsed_url['repo']}...")
        issue_data = get_issue_details(parsed_url['owner'], parsed_url['repo'], int(issue_number_str))
        
        print("Analyzing with AI...")
        analysis_result = analyze_issue(issue_data)
        
        print("\nAnalysis Result:")
        print(json.dumps(analysis_result, indent=2))

    except ValueError as ve:
         print(f"Error: {ve}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
