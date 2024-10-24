import docker
import time
from datetime import datetime

# Initialize Docker client
client = docker.DockerClient(base_url='unix:///home/ashuthe1/.docker/desktop/docker.sock')

# Function to list all active containers in a detailed format
def list_containers():
    containers = client.containers.list()
    
    print(f"{'='*40}")
    print(f"Container Status Log at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*40}")
    
    if len(containers) == 0:
        print("No active containers.")
        return
    
    for container in containers:
        print(f"Container Name : {container.name}")
        print(f"Container ID   : {container.short_id}")
        print(f"Status         : {container.status}")
        print(f"Image          : {container.image.tags[0]}")
        print(f"Created        : {container.attrs['Created']}")
        print(f"Ports          : {container.attrs['NetworkSettings']['Ports']}")
        print(f"Uptime         : {container.attrs['State']['StartedAt']}")
        print(f"{'-'*40}")

# Function to check the health of the Flask container
def check_flask_health():
    try:
        container = client.containers.get("devops-flask-app-1")  # Assuming Flask container is named 'devops-flask-app-1'
        # If health information is available, check its status
        status = container.status
        
        # If the container is unhealthy or not running, restart it
        if container.status != 'running':
            print(f"Restarting unhealthy Flask container: {container.short_id}")
            container.restart()
            print(f"Container '{container.name}' restarted successfully.\n{'='*40}")
        else:
            print(f"Flask container '{container.name}' is healthy and running.\n{'='*40}")
    
    except docker.errors.NotFound:
        print("Flask container not found.\n{'='*40}")

# Function to check the health of the MongoDB container
def check_mongo_health():
    try:
        container = client.containers.get("devops-mongo-1")
        status = container.status
        
        # If the container is unhealthy or not running, restart it
        if container.status != 'running':
            print(f"Restarting unhealthy MongoDB container: {container.short_id}")
            container.restart()
            print(f"Container '{container.name}' restarted successfully.\n{'='*40}")
        else:
            print(f"MongoDB container '{container.name}' is healthy and running.\n{'='*40}")
    
    except docker.errors.NotFound:
        print("Flask container not found.\n{'='*40}")

if __name__ == "__main__":
    while True:
        list_containers()           # List the status of all containers
        check_flask_health()        # Check and manage the Flask container's health
        check_mongo_health()        # Check and manage the Flask container's health
        time.sleep(10)              # Wait for 10 seconds before repeating
