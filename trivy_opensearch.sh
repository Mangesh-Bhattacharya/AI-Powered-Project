#!/bin/bash

# Run Trivy file system scan on OpenSearch directories

# Run Trivy on OpenSearch directories and save results
trivy fs /usr/share/opensearch/ >> /tmp/opensearch_1.txt --scanners vuln --include-dev-deps
trivy fs /etc/opensearch/ >> /tmp/opensearch_1.txt --scanners vuln --include-dev-deps
trivy fs /var/lib/opensearch/ >> /tmp/opensearch_1.txt --scanners vuln --include-dev-deps
trivy fs /opt/opensearch/ >> /tmp/opensearch_1.txt --scanners vuln --include-dev-deps

# Run Trivy on OpenSearch Dashboards directories and save results
trivy fs /usr/share/opensearch-dashboards/ >> /tmp/opensearch_dashboards_1.txt --scanners vuln --include-dev-deps
trivy fs /etc/opensearch-dashboards/ >> /tmp/opensearch_dashboards_1.txt --scanners vuln --include-dev-deps
trivy fs /var/lib/opensearch-dashboards/ >> /tmp/opensearch_dashboards_1.txt --scanners vuln --include-dev-deps
trivy fs /opt/opensearch-dashboard/ >> /tmp/opensearch_dashboards_1.txt --scanners vuln --include-dev-deps

# Notification
echo "Trivy scan completed."
