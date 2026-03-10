import subprocess
from vulnllama.ai import analyze_vulnerabilities

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
    
    print("\nAI Analysis:\n")
    ai_result = scan_dependencies(scan_output)
    print(ai_result)
