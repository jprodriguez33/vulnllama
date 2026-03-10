import sys
from sca import scan_dependencies

def main():

    if len(sys.argv) < 2:
        print("Usage: vulnclaw scan <path>")
        return

    command = sys.argv[1]

    if command == "scan":
        path = sys.argv[2] if len(sys.argv) > 2 else "."
        scan_dependencies(path)

if __name__ == "__main__":
    main()