import subprocess
import json
import csv
import datetime
import os
from vulnllama.ai import analyze_vulnerabilities
from vulnllama.vulnintel import get_cvss, get_epss
from vulnllama.osv_installer import ensure_osv_scanner_installed, get_osv_scanner_path

def scan_dependencies(path, output_format="text", ai=False):

    results = []
    print(f"Scanning dependencies in {path}")
    
    # Ensure osv-scanner is installed
    if not ensure_osv_scanner_installed():
        print("ERROR: Failed to install osv-scanner. Aborting scan.")
        return
    
    osv_path = get_osv_scanner_path()
    print("Running OSV Scanner...\n")

    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"reports/scan_report_{timestamp}.txt"
    report = open(report_path, "w")

    result = subprocess.run(
            [osv_path, "-r", path, "--format", "json"],
            capture_output=True,
            text=True
    )
    scan_output = result.stdout

    if not scan_output.strip():
        print("No vulns found")
        report.close()
        return
    
    try:
        data = json.loads(scan_output)
    except json.JSONDecodeError as e:
        print("OSV JSON parsing error:", e)
        print("Raw output:")
        print(scan_output[:500])
        report.close()
        return
    vulns = set()

    for result in data.get("results", []):
        for pkg in result.get("packages", []):
            for group in pkg.get("groups", []):

                for alias in group.get("aliases", []):
                    if alias.startswith("CVE"):
                        vulns.add(alias)

    if not vulns:
        print("No vulnerabilities found.")
        report.close()
        return
    
    print("\nDetected vulnerabilities:\n")
    
    for vuln in sorted(vulns):

        print(f"\n--- {vuln} ---")

        print("Getting CVSS...")
        cvss = get_cvss(vuln)
        print("Getting EPSS...")
        epss = get_epss(vuln)

        print(f"CVSS: {cvss}")
        print(f"EPSS: {epss}")

        is_high_risk = (cvss is not None and cvss >= 7) or (epss is not None and epss >= 0.1)
        analysis = ""

        if is_high_risk:
            print("\nvulnllama detects high risk vulnerability\n")
            if ai:
                print("\nAI Analysis:\n")
                ai_result = analyze_vulnerabilities(vuln)
                analysis = ai_result or "AI analysis returned no data"
                print(analysis)
                report.write("AI Analysis:\n")
                report.write(analysis + "\n\n")
            else:
                analysis = "High severity vulnerability; AI analysis skipped. Use --ai to include LLM output."
                print("AI analysis skipped (opt-in only).")
        else:
            analysis = "Low severity vulnerability; no AI analysis."
            print("Skipping vulnllama analysis due to low priority vulnerability")

        results.append({
            "cve": vuln,
            "cvss": cvss,
            "epss": epss,
            "analysis": analysis
        })

        report.write(f"{vuln} - CVSS: {cvss} - EPSS: {epss} - Analysis: {analysis}\n")

    report.close()

    # Export results in different formats
    if output_format == "json":
        export_path = f"reports/scan_report_{timestamp}.json"
        with open(export_path, "w") as f:
            json.dump(results, f, indent=4)
        print(f"\nJSON report saved to: {export_path}")

    elif output_format == "csv":
        export_path = f"reports/scan_report_{timestamp}.csv"
        with open(export_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["cve","cvss","epss","analysis"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\nCSV report saved to: {export_path}")

    elif output_format == "html":
        export_path = f"reports/scan_report_{timestamp}.html"
        with open(export_path, "w") as f:

            f.write("<html><body>")
            f.write("<h1>VulnLlama Report</h1>")
            f.write("<table border='1'>")
            f.write("<tr><th>CVE</th><th>CVSS</th><th>EPSS</th><th>AI Analysis</th></tr>")

            for r in results:
                f.write(
                    f"<tr><td>{r['cve']}</td><td>{r['cvss']}</td><td>{r['epss']}</td><td>{r['analysis']}</td></tr>"
                )

            f.write("</table></body></html>")

        print(f"\nHTML report saved to: {export_path}")

    print(f"\nText report saved to: {report_path}")