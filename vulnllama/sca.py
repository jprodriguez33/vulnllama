import subprocess
import json
from ai import analyze_vulnerabilities

def scan_dependencies(path):

    print(f"Scanning dependencies in {path}")

    
    result = subprocess.run(
            ["osv-scanner", "scan","source","-r", path, "--format", "json"],
            capture_output=True,
            text=True
    )
    scan_output = result.stdout

    if not scan_output.strip():
        print("No vulns found")
        return
    
    data = json.loads(scan_output)

    vulns = []

    for result in data.get("results", []):
        for vuln in result.get("vulnerabilities", []):
            vulns.append(vuln["id"])

    if not vulns:
        print("No vulnerabilities found.")
        return

    vuln_list = "\n".join(vulns)

    print("\nDetected vulnerabilities:\n")
    print(vuln_list)

    print("\nAI Analysis:\n")

    ai_result = analyze_vulnerabilities(vuln_list)

    print(ai_result)