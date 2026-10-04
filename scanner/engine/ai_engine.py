from google import genai
import json

client = genai.Client()


def explain_issues(code, issues):
    prompt = f"""
You are reviewing Roblox Luau code for security issues.

Code:
{code}

Detected issues:
{issues}

Return ONLY valid JSON.

For each detected issue return:
- ruleID
- risk
- fix
- example

Use this exact format:

[
    {{
        "ruleID": "P007",
        "risk": "Explain why this issue is dangerous.",
        "fix": "Explain how to fix it safely.",
        "example": "Give a short safer Luau code example."
    }}
]
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return json.loads(interaction.output_text)