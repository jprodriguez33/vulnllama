import sys
from vulnllama.sca import scan_dependencies
from vulnllama.github_scan import scan_github_repo
from vulnllama.osv_installer import ensure_osv_scanner_installed
from colorama import Fore, Style


def main():


    if len(sys.argv) == 1:
        banner()
        return  
    command = sys.argv[1]

    output_format = "text"
    ai_mode = False

    if "--json" in sys.argv:
        output_format = "json"
    elif "--csv" in sys.argv:
        output_format = "csv"
    elif "--html" in sys.argv:
        output_format = "html"

    if "--ai" in sys.argv:
        ai_mode = True

    if command == "setup":
        print("Setting up vulnllama dependencies...\n")
        if ensure_osv_scanner_installed():
            print("\n✅ vulnllama setup complete!")
        else:
            print("\n❌ Setup failed. Please check your internet connection and try again.")
            sys.exit(1)

    elif command == "scan":

        path = sys.argv[2] if len(sys.argv) > 2 else "."

        if path.startswith("https://github.com"):
            scan_github_repo(path, output_format, ai=ai_mode)
        else:
            scan_dependencies(path, output_format, ai=ai_mode)

    elif command == "--help" or command == "-h" or command == "help":
        banner()

    else:
        print("Unknown command\n")
        banner()

def banner():
    print(r"""

                    ⠀    /\  /\
                        ( •  • ) - I see your dependency vulnerabilities...
                        |> V  <|
                         \ -- /
                         |VULN|
                         |    | 
                          ____
          
        ██    ██ ██    ██ ██      ███    ██ ██       ██       █████  ███    ███  █████
        ██    ██ ██    ██ ██      ████   ██ ██       ██      ██   ██ ████  ████ ██   ██
        ██    ██ ██    ██ ██      ██ ██  ██ ██       ██      ███████ ██ ████ ██ ███████
         ██  ██  ██    ██ ██      ██  ██ ██ ██       ██      ██   ██ ██  ██  ██ ██   ██
          ████    ██████  ███████ ██   ████ ███████  ███████ ██   ██ ██      ██ ██   ██

                 VulnLlama - Local Vulnerability Intelligence Engine
                        CVE • EPSS • AI Analysis

Usage:
    vulnllama setup                                 (Download osv-scanner)
    vulnllama scan <path>                           (Scan local directory)
    vulnllama scan <path> --ai                      (Scan with AI analysis)
    vulnllama scan <github_repo>                    (Scan GitHub repository)
    vulnllama scan <path> [--json|--csv|--html]    (Choose output format)

Examples:
    vulnllama setup
    vulnllama scan .
    vulnllama scan . --ai
    vulnllama scan . --json
    vulnllama scan https://github.com/juice-shop/juice-shop

Created by JP Rodriguez
    """)

if __name__ == "__main__":
    main()