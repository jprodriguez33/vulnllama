import subprocess

def scan_dependencies(path):

    print(f"Scanning dependencies in {path}")

    try:
        result = subprocess.run(
            ["osv-scanner", "scan","source","-r", path, "--format", "json"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except FileNotFoundError:
        print("OSV Scanner not installed.")