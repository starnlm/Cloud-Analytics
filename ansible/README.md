1. You must have python3, pip, ansible and sudo on your pc
2. Replace the openrc.sh file with your own openrc.sh file generated off MRC. Save the password
3. Replace instance_key_name in mrc.yaml with your own key with public key uploaded to MRC.
3. a. your private key must be in ~/.ssh/ or you can change the variable in host_vars
4. a. run "up.sh" to deploy, some input required.


Notes:

This deployment only scales up. Scaling down is not supported and may cause some issues if you input 
a number lower than the current number of machines deployed. To properly scale down, couchdb shards 
have to be transferred from the machines that are to be shut down and then the machines removed from 
the cluster. Any other system applications on removed machines also have to be started on existing nodes.