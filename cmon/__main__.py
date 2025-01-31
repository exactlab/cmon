from argparse import ArgumentParser


parser = ArgumentParser(
    prog="cmon",
    description="""\
Collect metrics on CPU, memory, context switches and number of threads
from running containers, optionally filtering by Docker Compose project.
""",
    epilog="Copyright (C) 2024 eXact lab S.r.l. <https://exact-lab.it>\n",
)
subpparser = parser.add_subparsers(title="Commands", dest="cmd")
parser_plot = subpparser.add_parser("plot", help="Plot metrics")
parser_plot.add_argument("input_file", help="Path to HDF5 input file")
parser_plot.add_argument(
    "--host",
    help="Host on which to bind the Dash dashboard",
    default="127.0.0.1",
)

parser_monitor = subpparser.add_parser(
    "monitor", help="Record metrics [default behaviour]"
)
parser_monitor.add_argument(
    "-c", "--compose", help="If provided, filter by Docker Compose project"
)
parser_monitor.add_argument(
    "--no-docker",
    default=False,
    action="store_true",
    help="Do not search for Docker containers.",
)
parser_monitor.add_argument(
    "--pids", nargs="+", help="Process IDs to include in the analysis"
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


def main():
    args, _ = parser.parse_known_args()
    if args.cmd is None:
        args = parser_monitor.parse_args()
        args.cmd = "monitor"

    if args.cmd == "monitor":
        from ._monitor import Monitor
        from datetime import datetime
        from pathlib import Path
        from time import sleep

        process_map = {}
        if not args.no_docker:
            from ._docker import ComposeContainers

            cc = ComposeContainers(compose_project=args.compose)
            process_map.update(cc.process_map)

        mon = Monitor(process_map, pids=args.pids, buffer_size=args.buffer)
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
                    dest = Path(f"./{timestamp}.hdf5")
                mon.save(dest)
                return 0

    elif args.cmd == "plot":
        from ._plot import App
        import h5py

        with h5py.File(args.input_file, "r") as data:
            app = App(data)
            app.run(debug=True, host=args.host)
        return 0


if __name__ == "__main__":
    exit(main())
