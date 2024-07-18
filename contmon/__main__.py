from ._docker import ComposeContainers
from .monitor import Monitor
from time import sleep
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime


parser = ArgumentParser(
    prog="contmon",
    description="""The container monitor

Collect metrics on CPU, memory, context switches and number of threads 
for running containers, optionally filtering by Docker Compose project.
""",
)
parser.add_argument(
    "-c", "--compose", help="If provided, filter by Docker Compose project"
)
parser.add_argument(
    "-p",
    "--period",
    type=float,
    default=0.1,
    help="Sampling period [default=0.1s]",
)
parser.add_argument(
    "-o", "--output", help="Output path [defaults to ./<timestamp>.hdf5]"
)
parser.add_argument(
    "--buffer",
    type=int,
    default=1024,
    help="Length of measurement buffer [default=1024]",
)


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

    cc = ComposeContainers(compose_project=args.compose)

    mon = Monitor(cc.process_map, buffer_size=args.buffer)
    while True:
        try:
            mon.poll()
            sleep(args.period)
        except KeyboardInterrupt:
            try:
                dest = Path(args.output)
            except TypeError:
                now = datetime.now()
                timestamp = now.strftime("%Y%m%dT%H%M")
                dest = Path( f"./{timestamp}.hdf5")
            mon.save(dest)
            exit(0)
