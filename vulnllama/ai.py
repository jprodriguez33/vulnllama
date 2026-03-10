import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def analyze_vulnerabilities(scan_output):

    prompt = f"""
You are a senior application security engineer.

The following JSON is output from a software composition analysis scan.

Your task:
- Extract the vulnerabilities
- Explain what each vulnerability means
- Describe possible attack scenarios
- Suggest remediation steps

Ignore the JSON structure and schema.

Focus ONLY on the vulnerabilities listed in the report.

Scan results:
{scan_output}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]