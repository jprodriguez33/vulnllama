import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"

def analyze_vulnerabilities(scan_output):

    prompt = f"""
You are a cybersecurity vulnerability analyst.

Explain the vulnerabilities found in the following SCA scan.

For each vulnerability include:
- vulnerability description
- possible attack scenario
- exploitability estimate
- recommended fix

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