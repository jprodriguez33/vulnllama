# vulnllama

**Local Vulnerability Intelligence Engine** — Combines dependency scanning with optional AI analysis

Scans your dependencies for known vulnerabilities, enriches them with CVSS/EPSS severity scores, and optionally explains security impact using a local LLM.

## Features

-  **Dependency Scanning** — Uses OSV Scanner to detect vulnerable packages
-  **Severity Scoring** — Fetches CVSS & EPSS data for prioritization  
-  **Optional AI Analysis** — Run `--ai` flag to explain vulnerabilities with local LLM
-  **Local & GitHub Support** — Scan local directories or clone and scan GitHub repos
-  **Multiple Export Formats** — Generate reports as JSON, CSV, HTML, or text

## Installation

```bash
# Clone the repository
git clone https://github.com/jprodriguez33/vulnllama
cd vulnllama

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Initial Setup

Download the OSV Scanner binary for your platform:

```bash
vulnllama setup
```

This downloads the appropriate binary to `~/.vulnllama/osv-scanner/`. 
(Alternatively, it auto-downloads on first scan if missing.)

## Usage

### Basic Scan (No AI)

```bash
vulnllama scan .
```

### Scan with AI Analysis

For detailed vulnerability explanations (requires Ollama running locally):

```bash
vulnllama scan . --ai
```

### GitHub Repository Scan

```bash
vulnllama scan https://github.com/juice-shop/juice-shop
vulnllama scan https://github.com/juice-shop/juice-shop --ai
```

### Export Formats

```bash
vulnllama scan . --json
vulnllama scan . --csv
vulnllama scan . --html
```

## Example Output

```
Detected vulnerabilities:

--- CVE-2023-26486 ---
Getting CVSS...
Getting EPSS...
CVSS: 7.5
EPSS: 0.456

vulnllama detects high risk vulnerability

AI analysis skipped (opt-in only).
Use --ai flag to include LLM analysis.
```

**With `--ai` flag**, high-risk CVEs include:
```
AI Analysis:

Explanation of CVE - This vulnerability allows remote attackers to ...
Attack scenarios - An attacker could exploit this by ...
Remediation steps - Update the package to version X.Y.Z or later ...
```

## Requirements

- **Python 3.7+**
- **For AI analysis**: Ollama running locally on `http://localhost:11434`
  - Install: https://ollama.ai
  - Run: `ollama serve` + `ollama pull mistral`

## Project Roadmap

- [ ] CISA Known Exploited Vulnerabilities (KEV) integration
- [ ] Proof-of-Concept (PoC) generation for high-risk CVEs
- [ ] Support for additional package ecosystems
- [ ] Performance optimizations for large scans

## Disclaimer

This project is experimental and intended for **research and educational purposes only**. Use responsibly.
