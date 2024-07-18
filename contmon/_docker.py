from docker import DockerClient

class ComposeContainers:
    def __init__(self, *, compose_project: str | None = None):
        self.client = DockerClient()
        self.compose_project = compose_project

        if compose_project:
            self.containers = self.client.containers.list(
                filters={
                    "label": f"com.docker.compose.project={compose_project}"
                }
            )
        else:
            self.containers = self.client.containers.list()
        self._get_pids()
        self.process_map = {c.name: c.pid for c in self.containers}

    def _get_pids(self):
        for c in self.containers:
            c.pid = c.attrs["State"]["Pid"]
