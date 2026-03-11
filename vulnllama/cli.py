import sys
from vulnllama.sca import scan_dependencies
from vulnllama.github_scan import scan_github_repo
from colorama import Fore, Style


def main():


    if len(sys.argv) == 1:
        banner()
        return  
    command = sys.argv[1]

    if command == "scan":

        path = sys.argv[2] if len(sys.argv) > 2 else "."

        if path.startswith("https://github.com"):
            scan_github_repo(path)
        else:
            scan_dependencies(path)

    else:
        print("Unknown command\n")
        banner()

def banner():
    print(r"""

                    ⠀⢰⡏⢹⡆⠀⠀⠀⢰⡏⢹⡆⠀
⠀                    ⢸⡇⣸⡷⠟⠛⠻⢾⣇⣸⡇⠀
                    ⢠⡾⠛⠉⠁⠀⠀⠀⠈⠉⠛⢷⡄
                    ⣿⠀⢀⣄⢀⣠⣤⣄⡀⣠⡀⠀⣿
                    ⢻⣄⠘⠋⡞⠉⢤⠉⢳⠙⠃⢠⡿
                    ⣼⠃⠀⠀⠳⠤⠬⠤⠞⠀⠀⠘⣷
                    ⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿
                    ⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
                    ⢸⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿
          
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