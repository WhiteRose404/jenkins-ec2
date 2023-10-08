import jenkins
import yaml
import os
JENKINS_URL = os.environ.get('JENKINS_URL', '')
server = jenkins.Jenkins("http://52.47.203.240:8080/", username='admin', password='admin')



def get_nodes() -> dict:
    """
    Get the nodes from the config file
    """
    inventory = {}
    with open('../ansible/inventory.yml', 'r') as f:
        inventory = yaml.safe_load(f)
    slaves = inventory['slaves']['hosts'];
    return slaves;

# Extract the servers from the config file
slaves = get_nodes();

index = 1;
# Create a new node
for name in slaves:   
    slave = slaves[name];
    server.create_node(
        f'slave-{index}', 
        nodeDescription='EC2 Slave',
        remoteFS='/var/jenkins',
        labels=f'slave-{index}', 
        exclusive=False, 
        launcher=jenkins.LAUNCHER_SSH, 
        launcher_params={
            'port': '22', 
            'username': slave['ansible_user'],
            'credentialsId': 'f618241d-7931-4a4b-b7f4-687964e9d334',
            'host': slave['ansible_host'],
        });
    index += 1;