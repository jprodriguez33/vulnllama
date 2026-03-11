import sys
from vulnllama.sca import scan_dependencies
from vulnllama.github_scan import scan_github_repo
from colorama import Fore, Style


def main():


    if len(sys.argv) == 1:
        banner()
        return  
    command = sys.argv[1]

    output_format = "text"

    if "--json" in sys.argv:
        output_format = "json"
    elif "--csv" in sys.argv:
        output_format = "csv"
    elif "--html" in sys.argv:
        output_format = "html"

    if command == "scan":

        path = sys.argv[2] if len(sys.argv) > 2 else "."

        if path.startswith("https://github.com"):
            scan_github_repo(path, output_format)
        else:
            scan_dependencies(path, output_format)

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
    vulnllama scan <path>
    vulnllama scan <github_repo>

Example:
    vulnllama scan https://github.com/juice-shop/juice-shop

Created by JP Rodriguez
    """)

if __name__ == "__main__":
    main()