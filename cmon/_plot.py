from dash import Dash, dcc

class App:
    def __init__(self, hdf5_fp):
        self.fp = hdf5_fp
        self.app = Dash()
        self.app.layout = [
            dcc.Graph(
                id="graph_ucpu",
                figure=dict(
                    data=self._cpu_usage("time_user"),
                    layout=dict(title="User CPU"),
                ),
            ),
            dcc.Graph(
                id="graph_scpu",
                figure=dict(
                    data=self._cpu_usage("time_system"),
                    layout=dict(title="System CPU"),
                ),
            ),
            dcc.Graph(
                id="graph_iowait",
                figure=dict(
                    data=self._cpu_usage("time_iowait"),
                    layout=dict(title="IO wait CPU"),
                ),
            ),
            dcc.Graph(
                id="graph_mem_res",
                figure=dict(
                    data=self._metric("mem_rss"),
                    layout=dict(title="Memory RES"),
                ),
            ),
        ]

    def _cpu_usage(self, metric):
        def derivative(grp_data, key):
            t_ns = grp_data["timestamp_ns"][:]
            t = (t_ns - t_ns[0]) / 1e9

            cputime = grp_data[key][:]
            cpu_usage = (cputime[1:] - cputime[0:-1]) / (t[1:] - t[0:-1])
            return dict(x=t[1:], y=cpu_usage)

        data = []
        for grp, grp_data in self.fp.items():
            this_data = derivative(grp_data, metric)
            this_data["name"] = grp
            data.append(this_data)
        return data

    def _metric(self, metric):
        def linear(grp_data, key):
            t_ns = grp_data["timestamp_ns"][:]
            t = (t_ns - t_ns[0]) / 1e9

            mem = grp_data[key][:]
            return dict(x=t, y=mem)

        data = []
        for grp, grp_data in self.fp.items():
            this_data = linear(grp_data, metric)
            this_data["name"] = grp
            data.append(this_data)
        return data

    def run(self, **kwargs):
        self.app.run(**kwargs)
