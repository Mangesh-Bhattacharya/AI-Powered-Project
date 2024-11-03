import os
import subprocess
import datetime
import pandas as pd
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# Email configuration
smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server
smtp_port = '587'  # Replace with the correct port
smtp_user = 'recipient2@example.com'  # Replace with your email
recipient_emails = ['recipient2@example.com', 'recipient2@example.com']
subject = 'Latest Trivy Vulnerability Scan Results'

# Function to run Trivy scan


def run_trivy_scan():
    with open(output_txt, "w") as f:
        for directory in directories:
            subprocess.run(["trivy", "fs", directory, "--scanners",
                        "vuln", "--include-dev-deps"], stdout=f)

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
        data.append([cve_id, severity, description, date, time,
                    "Please refer to the CVE details for specific commands."])

    df = pd.DataFrame(data, columns=[
                    "CVE", "Threat Level", "Description", "Date", "Time", "Mitigation Commands"])
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

# Function to send email notification


def send_email(cves):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    body = f"Trivy Vulnerability Scan Results - {date} {time}\n\n"
    for cve in cves:
        body += f"CVE: {cve['CVE']}\n"
        body += f"Threat Level: {cve['Threat Level']}\n"
        body += f"Description: {cve['Description']}\n"
        body += f"Date: {date}\n"
        body += f"Time: {time}\n"
        body += f"Mitigation Commands: Please refer to the CVE details for specific commands.\n"
        body += "\n"

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.set_debuglevel(1)  # Enable debug output
        print("Sending email...")
        server.sendmail(smtp_user, recipient_emails, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function to run the scan, save the threat table, and send email notification


def main():
    print("Running Trivy scan...")
    run_trivy_scan()
    print("Parsing Trivy results...")
    cves = parse_trivy_results()
    print("Saving threat table in CSV format...")
    save_threat_table_csv(cves)
    print("Saving threat table in JSON format...")
    save_threat_table_json(cves)
    print("Sending email notification...")
    send_email(cves)


if __name__ == "__main__":
    main()
