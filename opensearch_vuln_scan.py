import os
import subprocess
import datetime
import pandas as pd
import json

# Directories to scan
directories = [
    "/usr/share/opensearch-dashboards/",
    "/etc/opensearch-dashboards/",
    "/var/lib/opensearch-dashboards/",
    "/opt/opensearch-dashboard/"
]

# Output files
output_txt = "/tmp/opensearch_dashboards_1.txt"
output_csv = "/tmp/threat_table.csv"
output_json = "/tmp/threat_table.json"

# Function to run Trivy scan
def run_trivy_scan():
    with open(output_txt, "w") as f:
        for directory in directories:
            subprocess.run(["trivy", "fs", directory, "--scanners", "vuln", "--include-dev-deps"], stdout=f)

# Function to parse Trivy scan results
def parse_trivy_results():
    with open(output_txt, "r") as f:
        lines = f.readlines()
    
    cves = []
    for line in lines:
        if "CVE-" in line:
            parts = line.split()
            cve = parts[0]
            severity = parts[1]
            description = " ".join(parts[2:])
            cves.append({
                "CVE": cve,
                "Threat Level": severity,
                "Description": description
            })
    
    return cves

# Function to save threat table in CSV format
def save_threat_table_csv(cves):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    
    data = []
    for cve in cves:
        cve_id = cve["CVE"]
        severity = cve["Threat Level"]
        description = cve["Description"]
        data.append([cve_id, severity, description, date, time, "Please refer to the CVE details for specific commands."])
    
    df = pd.DataFrame(data, columns=["CVE", "Threat Level", "Description", "Date", "Time", "Mitigation Commands"])
    df.to_csv(output_csv, index=False)

# Function to save threat table in JSON format
def save_threat_table_json(cves):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    
    data = []
    for cve in cves:
        cve_id = cve["CVE"]
        severity = cve["Threat Level"]
        description = cve["Description"]
        data.append({
            "CVE": cve_id,
            "Threat Level": severity,
            "Description": description,
            "Date": date,
            "Time": time,
            "Mitigation Commands": "Please refer to the CVE details for specific commands."
        })
    
    with open(output_json, "w") as f:
        json.dump(data, f, indent=2)

# Main function to run the scan and save the threat table
def main():
    run_trivy_scan()
    cves = parse_trivy_results()
    save_threat_table_csv(cves)
    save_threat_table_json(cves)

if __name__ == "__main__":
    main()
