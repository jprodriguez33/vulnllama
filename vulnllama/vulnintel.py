import requests

def get_cvss(cve):

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}"
    
    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            print(f"NVD request failed for {cve}")
            return None

        data = r.json()

        return data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]

    except requests.exceptions.JSONDecodeError:
        print(f"NVD returned invalid JSON for {cve}")
        return None

    except Exception as e:
        print(f"Error fetching CVSS for {cve}: {e}")
        return None

def get_epss(cve):

    url = f"https://api.first.org/data/v1/epss?cve={cve}"

    r = requests.get(url)
    data = r.json()

    return float(data["data"][0]["epss"])