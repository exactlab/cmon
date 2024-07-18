from ._docker import ComposeContainers
from .monitor import Monitor
from time import sleep


if __name__ == "__main__":
    cc = ComposeContainers()

    mon = Monitor(cc.process_map)
    while True:
        try:
            mon.poll()
            p0 = mon.processes[0]
            sleep(0.1)
        except KeyboardInterrupt:
            mon.save()
            exit(0)
