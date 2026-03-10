import subprocess
import json
from ai import analyze_vulnerabilities
from vulnintel import get_cvss, get_epss

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

    vulns = set()

    for result in data.get("results", []):
        for pkg in result.get("packages", []):
            for group in pkg.get("groups", []):

                for alias in group.get("aliases", []):
                    if alias.startswith("CVE"):
                        vulns.add(alias)

    if not vulns:
        print("No vulnerabilities found.")
        return
    
    print("\nDetected vulnerabilities:\n")
    
    for vuln in vulns:

        print(f"\n--- {vuln} ---")

        cvss = get_cvss(vuln)
        epss = get_epss(vuln)

        print(f"CVSS: {cvss}")
        print(f"EPSS: {epss}")

        if cvss and cvss >= 7:

            print("\nAI Analysis:\n")

            ai_result = analyze_vulnerabilities(vuln)

            print(ai_result)