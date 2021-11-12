#!/bin/bash

# Group 53, Melbourne, Perth, Uttar Pradesh
# Team Members: Aditi Basu 1178282, Kevin Van 995203, Linan Jia 806003, Nand Lal Mishra 1245159, Zhirui Liang 1255971

# Input number of instances so that mrc.yaml is updated with appropriate variables
if python3 create_instances.py; then
    echo "valid number"
else
    exit 1
fi

# run openrc.sh to access MRC. NOTE: REPLACE WITH YOUR OWN
. ./unimelb-comp90024-2021-grp-53-openrc.sh

# Create instances on MRC with some initial dependency installation. IPs kept in hosts.ini
ansible-playbook --ask-become-pass deploy-instances.yaml

# Group created instances into groups using hosts.ini and store in applications.ini
variable=$(python3 group_clusters.py)

# Install software according to applications.ini generated in previous step
ansible-playbook -i ./inventory/applications.ini setup-applications.yaml

echo "The website is hosted at: $variable"