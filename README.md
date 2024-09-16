# `cmon` - The container monitor

`cmon` collects metrics on running containers and saves them to an HDF5
file.

## Installation

Clone this repository and run `poetry install`. Afterwards you will be able to
invoke `cmon` as `poetry run cmon`.

You may alternatively build a Python wheel for `cmon` and install it system
wide as follows, assuming you are in the repository root:

```bash
poetry build
pip install dist/cmon-0.1.0-py3-none-any.whl
```

From then on you should have `cmon` available in your path.

## Collection

```
python -m cmon -h

usage: cmon monitor [-h] [-c COMPOSE] [-p PERIOD] [-o OUTPUT]
                       [--buffer BUFFER]

options:
  -h, --help            show this help message and exit
  -c COMPOSE, --compose COMPOSE
                        If provided, filter by Docker Compose project
  -p PERIOD, --period PERIOD
                        Sampling period [default=0.1s]
  -o OUTPUT, --output OUTPUT
                        Output path [defaults to ./<timestamp>.hdf5]
  --buffer BUFFER       Length of measurement buffer [default=1024]
```

## Plotting

Experimental plotting based on Dash.

```
usage: cmon plot [-h] input_file

positional arguments:
  input_file  Path to HDF5 input file

options:
  -h, --help  show this help message and exit
```

The (interactive) plots should show up in `http://localhost:8050`.
