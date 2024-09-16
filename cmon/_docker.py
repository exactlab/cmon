from docker import DockerClient
from psutil import Process


class ComposeContainers:
    def __init__(self, *, compose_project=None):
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
            # NOTE (jacopo): For reasons I don't know, if the root process is a
            # shell, the metrics of the root process *do not* include the
            # children. In this case we take the first (and usually only)
            # child.
            root_process = Process(c.attrs["State"]["Pid"])
            if root_process.name() == "sh":
                c.pid = root_process.children()[0].pid
            else:
                c.pid = root_process.pid
