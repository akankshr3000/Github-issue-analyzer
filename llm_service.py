import os
import json
from openai import OpenAI
from typing import Dict, Any

def analyze_issue(issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sends issue data to OpenAI to generate a structured analysis.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not found.")

    client = OpenAI(api_key=api_key)

    system_prompt = """You are an expert software engineering assistant. 
    Analyze the GitHub issue provided and return ONLY a valid JSON object with the following structure:
    {
      "summary": "A one-sentence summary of the user's problem or request.",
      "type": "bug | feature_request | documentation | question | other",
      "priority_score": "A score from 1 (low) to 5 (critical), with a short justification.",
      "suggested_labels": ["2-3 relevant GitHub labels"],
      "potential_impact": "Brief description of impact if the issue is a bug."
    }
    
    Do NOT output markdown code blocks (like ```json). Just the raw JSON string.
    Do NOT include any explanations or extra text.
    Ensue valid JSON syntax.
    """

    user_content = f"""
    Title: {issue_data['title']}
    Author: {issue_data['user']}
    State: {issue_data['state']}
    
    Body:
    {issue_data['body'][:8000]} 
    
    Comments Snippets:
    {issue_data['comments'][:4000]}
    """
    # Truncating body and comments to avoid context limits, though 4o-mini/3.5-turbo usually handle 16k/128k.

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Cost effective and fast
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2, # Low temperature for more deterministic output
            max_tokens=500
        )

        content = response.choices[0].message.content.strip()
        
        # Strip potential markdown formatting if the model disobeys slightly
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        return json.loads(content.strip())
        
    except json.JSONDecodeError:
        # Fallback if model fails strict JSON
        raise Exception("AI failed to generate valid JSON. Raw Output: " + content)
    except Exception as e:
        raise Exception(f"OpenAI API Error: {str(e)}")
