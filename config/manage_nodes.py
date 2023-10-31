import jenkins
import yaml
import os
from dotenv import load_dotenv
load_dotenv()


JENKINS_URL = os.environ.get('JENKINS_URL', 'localhost')
USERNAME = os.environ.get('JENKINS_USERNAME', '')
PASSWORD = os.environ.get('JENKINS_PASSWORD', '')
server = jenkins.Jenkins(f"http://{JENKINS_URL}:8080/", username=USERNAME, password=PASSWORD)



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
            'credentialsId': '811a06f1-78f7-47bf-b072-cab4483bcc9d',
            'host': slave['ansible_host'],
        });
    index += 1;