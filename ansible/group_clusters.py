# Group 53, Melbourne, Perth, Uttar Pradesh
# Team Members: Aditi Basu 1178282, Kevin Van 995203, Linan Jia 806003, Nand Lal Mishra 1245159, Zhirui Liang 1255971

from shutil import copyfile

#Read in hosts.ini created by openstack roles
with open("./inventory/hosts.ini") as f:
    f.readline()
    nodes = f.read()


harvesters = frontend = backend = masternode = othernodes = nodes
nodes = nodes.split()

# Do the assigning here ( could be more complex )
n = len(nodes)
assert(n>=1)
if n==1:
    othernodes = ""
elif n==2:
    masternode = frontend = nodes[0]
    othernodes = harvesters = nodes[1]
else:
    masternode = frontend = nodes[0]
    othernodes = harvesters = "\n".join(nodes[1:])

# Write out each group into applications.ini
with open("./inventory/applications.ini", 'w') as f:
    f.write(("#IPs under each heading. To be created from hosts.ini with script\n"
            "[dbcluster:children]\n"
            "masternode\n"
            "othernodes\n\n"
            "[masternode]\n"
            f"{masternode}\n"
            "[othernodes]\n"
            f"{othernodes}\n"
            "[harvesters]\n"
            f"{harvesters}\n"
            "[frontend]\n"
            f"{frontend}\n"
            ))

# Copy config files to harvester for dynamic connection to database
copyfile("./inventory/applications.ini",  "../applications.ini")
copyfile("./inventory/applications.ini",  "../Harvester/StreamAPI/applications.ini")
copyfile("./inventory/applications.ini",  "../Harvester/SearchAPI/applications.ini")
# Print frontend for later use
print(frontend)