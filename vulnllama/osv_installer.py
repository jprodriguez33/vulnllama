import os
import sys
import platform
import subprocess
import shutil
import stat
import urllib.request
import json
import tempfile

OSV_SCANNER_DIR = os.path.expanduser("~/.vulnllama/osv-scanner")
OSV_SCANNER_BIN = os.path.join(OSV_SCANNER_DIR, "osv-scanner")

def get_platform_info():
    """Detect OS and architecture."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Map platform.machine() output to osv-scanner binary names
    if machine in ['amd64', 'x86_64']:
        arch = 'amd64'
    elif machine in ['arm64', 'aarch64']:
        arch = 'arm64'
    else:
        arch = machine
    
    if system == 'darwin':
        os_name = 'darwin'  # Keep darwin instead of macos for release naming
    elif system == 'linux':
        os_name = 'linux'
    elif system == 'windows':
        os_name = 'windows'
    else:
        os_name = system
    
    return os_name, arch

def get_osv_scanner_url():
    """Get the download URL for osv-scanner based on platform."""
    os_name, arch = get_platform_info()
    
    # Fetch latest release info from GitHub
    try:
        with urllib.request.urlopen("https://api.github.com/repos/google/osv-scanner/releases/latest") as response:
            release_data = json.loads(response.read())
            latest_version = release_data['tag_name']
            
            # Construct expected binary name and look for exact match
            if os_name == 'windows':
                binary_name = f"osv-scanner_{os_name}_{arch}.exe"
            else:
                binary_name = f"osv-scanner_{os_name}_{arch}"
            
            # Find matching asset by name
            for asset in release_data.get('assets', []):
                if asset['name'] == binary_name:
                    return asset['browser_download_url']
            
            # If no exact match, construct URL and rely on GitHub fallback
            url = f"https://github.com/google/osv-scanner/releases/download/{latest_version}/{binary_name}"
            return url
            
    except Exception as e:
        print(f"Failed to fetch latest osv-scanner version: {e}")
        return None

def ensure_osv_scanner_installed():
    """Check if osv-scanner is available, download if not."""
    
    # First, check if osv-scanner is already in PATH
    if shutil.which("osv-scanner"):
        print("osv-scanner found in PATH")
        return True
    
    # Check if already downloaded
    if os.path.exists(OSV_SCANNER_BIN):
        # Make sure it's executable
        st = os.stat(OSV_SCANNER_BIN)
        os.chmod(OSV_SCANNER_BIN, st.st_mode | stat.S_IEXEC)
        print(f"osv-scanner found at {OSV_SCANNER_BIN}")
        return True
    
    print("osv-scanner not found. Downloading...")
    
    # Create directory if it doesn't exist
    os.makedirs(OSV_SCANNER_DIR, exist_ok=True)
    
    # Get download URL
    url = get_osv_scanner_url()
    if not url:
        print("ERROR: Could not determine osv-scanner download URL")
        return False
    
    print(f"Downloading from: {url}")
    
    try:
        # Download to temporary file first
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
            with urllib.request.urlopen(url) as response:
                tmp.write(response.read())
        
        # Move to final location
        os.rename(tmp_path, OSV_SCANNER_BIN)
        
        # Make executable on Unix-like systems
        if sys.platform != 'win32':
            st = os.stat(OSV_SCANNER_BIN)
            os.chmod(OSV_SCANNER_BIN, st.st_mode | stat.S_IEXEC)
        
        print(f"osv-scanner installed successfully at {OSV_SCANNER_BIN}")
        return True
    
    except Exception as e:
        print(f"ERROR: Failed to download osv-scanner: {e}")
        # Clean up temp file if it exists
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
        return False

def get_osv_scanner_path():
    """Return the path to osv-scanner binary."""
    # Return from PATH if available, otherwise return downloaded path
    path_in_path = shutil.which("osv-scanner")
    if path_in_path:
        return path_in_path
    return OSV_SCANNER_BIN
