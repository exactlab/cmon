# `contmon` - The container monitor

`contmon` collects metrics on running containers and saves them to an HDF5
file.

## Collection

```
usage: contmon [-h] [-c COMPOSE] [-p PERIOD] [-o OUTPUT] [--buffer BUFFER]

The container monitor Collect metrics on CPU, memory, context switches and
number of threads for running containers, optionally filtering by Docker
Compose project.

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

Experimental plotting based on Dash. Run 

```python contmon/_plot.py [input.hdf5]```

and the (interactive) plots should show up in `http://localhost:8050`.


