from time import perf_counter_ns

import h5py
import numpy as np
from psutil import Process


class ProcessMonitor:
    def __init__(self, *, pid, display_name=None, buffer_size=1024):
        self.proc = Process(pid)
        self.display_name = display_name or self.proc.name()
        self.buffer_size = buffer_size

        self.idx = 0
        self.buffers = []
        self.columns = [
            "timestamp_ns",
            "time_user",
            "time_system",
            "time_iowait",
            "num_threads",
            "mem_rss",
            "mem_vms",
            "mem_shr",
            "ctx_vol",
            "ctx_invol",
        ]

    def get_buffer(self):
        buf = np.zeros((self.buffer_size, 10), dtype=float)
        self.buffers.append(buf)

    def poll(self):
        try:
            self.buffers[-1][self.idx] = self.poll_single()
        except IndexError:
            self.idx = 0
            self.get_buffer()
            self.buffers[-1][self.idx] = self.poll_single()
        self.idx += 1

    def poll_single(self):
        p = self.proc
        with p.oneshot():
            # NOTE (JN): requires root permissions
            # io = process.io_counters()
            mem = p.memory_info()
            cpu_times = p.cpu_times()
            ctx_switch = p.num_ctx_switches()
            out = [
                perf_counter_ns(),
                cpu_times.user,
                cpu_times.system,
                cpu_times.iowait,
                p.num_threads(),
                mem.rss,
                mem.vms,
                mem.shared,
                ctx_switch.voluntary,
                ctx_switch.involuntary,
            ]
        return out

    def crop_buffer(self):
        self.buffers[-1] = self.buffers[-1][: self.idx]

    def save(self, hdf5_fp):
        self.crop_buffer()
        data = np.concatenate(self.buffers)
        grp = hdf5_fp.create_group(self.display_name)
        for i, col in enumerate(self.columns):
            grp[col] = data[:, i]


class Monitor:
    def __init__(self, process_map, pids=None, buffer_size=1024):
        self.processes = [
            ProcessMonitor(display_name=name, pid=pid, buffer_size=buffer_size)
            for name, pid in process_map.items()
        ]
        if pids is not None:
            self.processes.extend(
                ProcessMonitor(pid=int(pid), buffer_size=buffer_size)
                for pid in pids
            )

    def poll(self):
        for p in self.processes:
            p.poll()

    def save(self, dest):
        with h5py.File(dest, "w") as f:
            for p in self.processes:
                p.save(f)
