import sys
from sca import scan_dependencies
from github_scan import scan_github_repo

def main():

    if len(sys.argv) < 2:
        print("Usage: vulnllama scan <path>")
        return

    command = sys.argv[1]

    if command == "scan":
        path = sys.argv[2] if len(sys.argv) > 2 else "."

        if path.startswith("https://github.com"):
            scan_github_repo(path)
        else:
            scan_dependencies(path)
    else:
        print("Unkown command")
        print("Usage: vulnllama scan <path-or-github-url")

if __name__ == "__main__":
    main()