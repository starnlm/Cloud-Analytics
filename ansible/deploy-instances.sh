#!/bin/bash
# Group 53, Melbourne, Perth, Uttar Pradesh
# Team Members: Aditi Basu 1178282, Kevin Van 995203, Linan Jia 806003, Nand Lal Mishra 1245159, Zhirui Liang 1255971

. ./unimelb-comp90024-2021-grp-53-openrc.sh; ansible-playbook --ask-become-pass deploy-instances.yaml

# Create applications.ini inventory file from hosts.ini
python3 group_clusters.py