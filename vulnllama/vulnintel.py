import requests

def get_cvss(cve):

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}"
    
    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            print(f"NVD request failed for {cve}")
            return None

        data = r.json()

        # Navigate to CVSS score, checking for cvssMetricV31 first, then other versions
        vuln_data = data.get("vulnerabilities", [])
        if not vuln_data:
            print(f"No vulnerability data for {cve}")
            return None

        metrics = vuln_data[0].get("cve", {}).get("metrics", {})
        
        # Try V3.1 metrics first (most common)
        if "cvssMetricV31" in metrics and metrics["cvssMetricV31"]:
            return metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
        
        # Fall back to V3.0 metrics
        if "cvssMetricV30" in metrics and metrics["cvssMetricV30"]:
            return metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]
        
        # Fall back to V2.0 metrics
        if "cvssMetricV2" in metrics and metrics["cvssMetricV2"]:
            return metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]
        
        print(f"No CVSS metrics available for {cve}")
        return None

    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing CVSS for {cve}: {e}")
        return None

    except requests.exceptions.JSONDecodeError:
        print(f"NVD returned invalid JSON for {cve}")
        return None

    except Exception as e:
        print(f"Error fetching CVSS for {cve}: {e}")
        return None

def get_epss(cve):

    url = f"https://api.first.org/data/v1/epss?cve={cve}"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            print(f"EPSS request failed for {cve}")
            return None

        data = r.json()

        # Check if data list exists and has entries
        if not data.get("data") or len(data["data"]) == 0:
            print(f"No EPSS data available for {cve}")
            return None

        return float(data["data"][0]["epss"])

    except requests.exceptions.JSONDecodeError:
        print(f"EPSS API returned invalid JSON for {cve}")
        return None

    except (KeyError, ValueError, TypeError) as e:
        print(f"Error parsing EPSS for {cve}: {e}")
        return None

    except Exception as e:
        print(f"Error fetching EPSS for {cve}: {e}")
        return None