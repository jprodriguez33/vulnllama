# vulnllama
AI-assisted software composition analysis.

Combines traditional dependency scanning with LLM reasoning to explain
vulnerability impact and exploitability.
# Features
Scans github repos for vulnerable dependencies using OSV-scanner
Grabs EPSS and CVSS data to filter low-priority vulnerabilities
Uses a local llm to explain vulnerabilities and PoC's
Generates reports to view

# Installation
Clone the repository:

git clone https://github.com/jprodriguez33/vulnllama
cd vulnllama

Create a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Install OSV Scanner:

https://github.com/google/osv-scanner

# Usage
Scan a local directory:

python vulnllama/cli.py scan .

Scan a GitHub repository:

python vulnllama/cli.py scan https://github.com/juice-shop/juice-shop

Example output:

Detected vulnerabilities:

--- CVE-2023-50728 ---
CVSS: 5.4
EPSS: 0.00479

--- CVE-2019-19844 ---
CVSS: 9.8
EPSS: 0.72

AI Analysis:
This vulnerability allows remote code execution due to improper input validation...
# To-Do 
Get data from exploit-db and cisa kev

PoC generation

support for more dependency ecosystems

performance optimizations

fix issue with NIST NVD not getting CVE properly

# Disclaimer
This project is experimental and is intended for research and education purposes
