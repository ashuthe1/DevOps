import docker
from docker.errors import NotFound

# Initialize Docker client
client = docker.DockerClient(base_url='unix:///home/ashuthe1/.docker/desktop/docker.sock')

# Network name and container names
network_name = 'flask_mongo_network'
flask_container_name = 'devops-flask-app-1'
mongo_container_name = 'devops-mongo-1'

def create_network():
    # Check if the network already exists
    try:
        network = client.networks.get(network_name)
        print(f"Network '{network_name}' already exists.")
    except NotFound:
        # Create the network if it doesn't exist
        print(f"Creating network '{network_name}'...")
        network = client.networks.create(network_name, driver="bridge")
        print(f"Network '{network_name}' created successfully.")
    
    return network

def connect_containers_to_network(network):
    # Connect Flask app container
    try:
        flask_container = client.containers.get(flask_container_name)
        network.connect(flask_container)
        print(f"Connected {flask_container_name} to the network.")
    except NotFound:
        print(f"Error: {flask_container_name} container not found.")
    
    # Connect MongoDB container
    try:
        mongo_container = client.containers.get(mongo_container_name)
        network.connect(mongo_container)
        print(f"Connected {mongo_container_name} to the network.")
    except NotFound:
        print(f"Error: {mongo_container_name} container not found.")

def inspect_network(network):
    # Inspect the network and list connected containers
    print(f"\nInspecting network '{network_name}'...")
    network_data = client.networks.get(network_name)
    
    print(f"Network ID: {network_data.id}")
    print(f"Containers connected to '{network_name}':")
    for container_id, container_info in network_data.attrs['Containers'].items():
        print(f"  Container ID: {container_id}")
        print(f"  Container Name: {container_info['Name']}")
        print(f"  IPv4 Address: {container_info['IPv4Address']}")
        print()

def manage_network():
    # Create network if it doesn't exist
    network = create_network()

    # Connect the containers to the network
    connect_containers_to_network(network)

    # Inspect and verify the network
    inspect_network(network)

if __name__ == "__main__":
    manage_network()
