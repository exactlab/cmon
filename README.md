# `contmon` - The container monitor

`contmon` collects metrics on running containers and saves them to an HDF5
file.

## Collection

```
python -m contmon -h

usage: contmon monitor [-h] [-c COMPOSE] [-p PERIOD] [-o OUTPUT]
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
usage: contmon plot [-h] input_file

positional arguments:
  input_file  Path to HDF5 input file

options:
  -h, --help  show this help message and exit
```

The (interactive) plots should show up in `http://localhost:8050`.


