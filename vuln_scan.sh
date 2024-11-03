#!/bin/bash

# Directories to scan
FLUENT_BIT_DIRS="/opt/fluentbit /var/spool/mail/fluentbit"
DATA_PREPPER_DIRS="/opt/dataprepper /var/spool/mail/dataprepper"
FLUENT_BIT_OUTPUT_DIR="/tmp/fluentbit_scans"
DATA_PREPPER_OUTPUT_DIR="/tmp/dataprepper_scans"
SCAN_OUTPUT_JSON="image_$(date +"%Y-%m-%d_%H-%M-%S").json"
SCAN_OUTPUT_CSV="image_$(date +"%Y-%m-%d_%H-%M-%S").csv"

# Ensure output directories exist
mkdir -p "$FLUENT_BIT_OUTPUT_DIR"
mkdir -p "$DATA_PREPPER_OUTPUT_DIR"

# Function to scan directories
scan_directories() {
    local directory="$1"
    local output_dir="$2"
    local output_json="$output_dir/$SCAN_OUTPUT_JSON"
    local output_csv="$output_dir/$SCAN_OUTPUT_CSV"

    echo "Scanning directory: $directory"
    trivy fs \
        --format json \
        --output "$output_file" \
        --severity CRITICAL,HIGH,MEDIUM,LOW \
        --quiet \
        "$directory"
}

# Function to scan Docker container
scan_docker_container() {
    local image="$1"
    local output_dir="$2"
    local output_json="$output_dir/$SCAN_OUTPUT_JSON"
    local output_csv="$output_dir/$SCAN_OUTPUT_CSV"

    echo "Scanning Docker container: $image"
    trivy image \
        --format json \
        --output "$output_file" \
        --severity CRITICAL,HIGH,MEDIUM,LOW \
        --quiet \
        "$image"
    
    # Convert JSON to CSV (or TXT)
    jq -r '.Results[] | [.Target, .Type, .Vulnerabilities[].Severity, .Vulnerabilities[].PkgName, .Vulnerabilities[].VulnerabilityID, .Vulnerabilities[].InstalledVersion, .Vulnerabilities[].FixedVersion] | @csv' "$output_json" > "$output_csv"
}

# Scan Fluent Bit directories
for dir in $FLUENT_BIT_DIRS; do
    scan_directories "$dir" "$FLUENT_BIT_OUTPUT_DIR"
done

# Scan Data Prepper directories
for dir in $DATA_PREPPER_DIRS; do
    scan_directories "$dir" "$DATA_PREPPER_OUTPUT_DIR"
done

# Scan Docker containers
scan_docker_container "fluent/fluent-bit" "$FLUENT_BIT_OUTPUT_DIR"
scan_docker_container "opensearchproject/data-prepper:2.7.0" "$DATA_PREPPER_OUTPUT_DIR"

echo "Vulnerability scan completed."
