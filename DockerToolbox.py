import requests, os, json

class DockerToolbox:

    def __init__(self,DOCKER_BASE_URL=os.environ['DOCKER_BASE_URL']):
        self.DOCKER_BASE_URL=DOCKER_BASE_URL
        self.CONTAINER_LIST=self.listContainers()
        self.CONTAINER_IDS=self.getIDs()

    def listContainers(self):
        containers = requests.get(self.DOCKER_BASE_URL+"/containers/json?all=True").json()
        self.updateContainerLists(containers)
        return containers

    def updateContainerLists(self,containers):
        self.CONTAINER_LIST=containers
        self.CONTAINER_IDS=self.getIDs()

    def restartContainer(self,CONTAINER_ID):
        RESTART_URL=f"{self.DOCKER_BASE_URL}/containers/{CONTAINER_ID}/restart"
        response = requests.post(RESTART_URL)
        if response.status_code != 204:
            return False
        else:
            return True

    def startContainer(self,CONTAINER_ID):
        START_URL=f"{self.DOCKER_BASE_URL}/containers/{CONTAINER_ID}/start"
        response = requests.post(START_URL)
        if response.status_code != 204:
            return False
        else:
            return True

    def getIDs(self):
        container_IDS = []
        for container in self.CONTAINER_LIST:
            container_IDS.append(container['Id'])
        return container_IDS

if __name__ == "__main__":
    dtb= DockerToolbox()
    print(json.dumps(dtb.CONTAINER_LIST,indent=3))