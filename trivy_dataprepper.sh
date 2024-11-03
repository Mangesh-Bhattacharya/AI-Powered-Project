#!/bin/bash

# dataprepper vulnerability scan
trivy fs /opt/dataprepper >> /tmp/dataprepper_scans/dataprepper_1.txt
trivy fs /var/spool/mail/dataprepper >> /tmp/dataprepper_var.txt
trivy image opensearchproject/data-prepper:2.0.1 >> /tmp/dataprepper_scans/

# fluentbit vulnerability scan
trivy fs /opt/fluentbit >> /tmp/fluentbit_scans/trivy_fluentbit_1.txt
trivy fs /var/spool/mail/fluentbit >> /tmp/fluentbit_scans/
trivy image fluent/fluent-bit >> /tmp/fluentbit_scans/

# Notification
echo "Trivy scan completed."