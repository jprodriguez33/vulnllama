import requests

def get_cvss(cve):

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}"
    
    r = requests.get(url)
    data = r.json()

    metrics = data["vulnerabilities"][0]["cve"]["metrics"]

    if "cvssMetricV31" in metrics:
        return metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]

    return None

def get_epss(cve):

    url = f"https://api.first.org/data/v1/epss?cve={cve}"

    r = requests.get(url)
    data = r.json()

    return float(data["data"][0]["epss"])