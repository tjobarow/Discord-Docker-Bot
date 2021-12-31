import requests, os, json

class DockerToolbox:

    def __init__(self,DOCKER_BASE_URL=os.environ['DOCKER_BASE_URL']):
        self.DOCKER_BASE_URL=DOCKER_BASE_URL

    def listContainers(self):
        containers = requests.get(self.DOCKER_BASE_URL+"/containers/json?all=True").json()
        for container in containers:
            print("~~~~~~~~~~~"*5)
            print(json.dumps(container,indent=3))
            print("~~~~~~~~~~~"*5)

    def restartContainer(self,CONTAINER_ID):
        RESTART_URL=f"{self.DOCKER_BASE_URL}/containers/{CONTAINER_ID}/restart"
        response = requests.post(RESTART_URL)
        if response.status_code is not 204:
            return False
        else:
            return True

    def startContainer(self,CONTAINER_ID):
        RESTART_URL=f"{self.DOCKER_BASE_URL}/containers/{CONTAINER_ID}/restart"
        response = requests.post(RESTART_URL)
        if response.status_code is not 204:
            return False
        else:
            return True

if __name__ == "__main__":
    listContainers()
    print(restartContainer("11534306ba62f374c4cc39574de797e87f945d2ae4db50e4b6de57662b7a9c45"))