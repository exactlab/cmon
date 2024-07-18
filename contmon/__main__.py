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
subpparser = parser.add_subparsers(title="Commands", dest="cmd")
parser_plot = subpparser.add_parser("plot", help="Plot metrics")
parser_plot.add_argument("input_file", help="Path to HDF5 input file")

parser_monitor = subpparser.add_parser(
    "monitor", help="Record metrics [default behaviour]"
)
parser_monitor.add_argument(
    "-c", "--compose", help="If provided, filter by Docker Compose project"
)
parser_monitor.add_argument(
    "-p",
    "--period",
    type=float,
    default=0.1,
    help="Sampling period [default=0.1s]",
)
parser_monitor.add_argument(
    "-o", "--output", help="Output path [defaults to ./<timestamp>.hdf5]"
)
parser_monitor.add_argument(
    "--buffer",
    type=int,
    default=1024,
    help="Length of measurement buffer [default=1024]",
)


if __name__ == "__main__":
    args, extra = parser.parse_known_args()
    if args.cmd is None:
        args = parser_monitor.parse_args()
        args.cmd = "monitor"

    if args.cmd == "monitor":
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

    elif args.cmd == "plot":
        from ._plot import App
        import h5py

        with h5py.File(args.input_file, "r") as data:
            app = App(data)
            app.run(debug=True)
        exit(0)
