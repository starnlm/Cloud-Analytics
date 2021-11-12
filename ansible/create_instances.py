# Group 53, Melbourne, Perth, Uttar Pradesh
# Team Members: Aditi Basu 1178282, Kevin Van 995203, Linan Jia 806003, Nand Lal Mishra 1245159, Zhirui Liang 1255971

import re 
from pathlib import Path

# Get number of machines to deploy
n = int(input("How many instances? "))
assert(n>0)

hosts_path = Path("inventory/hosts.ini")
if hosts_path.exists():
    with hosts_path.open() as f:
        hosts = f.read().split()[1:]
        if len(hosts) > n:
            with open("host_vars/delete.txt", 'w+') as f:
                f.write("\n".join(["cluster-{num}".format(num=i) for i in range(n+1,len(hosts)+1)]))

# Read in mrc.yaml to update
with open("host_vars/mrc.yaml", "r") as f:
    s = f.read()
# Replace volumes and instances with appropriate number.
with open("host_vars/mrc.yaml", "w") as f:
    volumes_regex = "(?:volumes:)((.|\n)*?)(?:#)"
    volumes = ("  - vol_name: cluster-{num}-1\n"
               "    vol_size: 10\n"
               "  - vol_name: cluster-{num}-2\n"
               "    vol_size: 10\n")
    volumes_string = "volumes:\n" + "".join([volumes.format(num=i) for i in range(1,n+1)]) + "\n#"
    s = re.sub(volumes_regex, volumes_string, s, 1)

    instances_regex = "(?:instances:)((.|\n)*?)(?:#)"
    instances = ("  - name: cluster-{num}\n"
                 "    volumes: ['cluster-{num}-1', 'cluster-{num}-2']\n")
    instances_string = "instances:\n" + "".join([instances.format(num=i) for i in range(1,n+1)]) + "\n#"
    s = re.sub(instances_regex, instances_string, s, 1)

    f.write(s)