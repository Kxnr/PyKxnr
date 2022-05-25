import pickle
import tracemalloc
import os
import datetime
from functools import wraps
import linecache

def take_snapshot(prefix=None, output_dir="."):
    snapshot = tracemalloc.take_snapshot()

    abspath = os.path.abspath(output_dir)
    os.makedirs(abspath, exist_ok=True)
    
    snapshot_file = os.path.join(abspath, f"{prefix or 'snapshot'}_{datetime.datetime.now().isoformat()}.snp")
    print(f"Saving memory usage snapshot to: {snapshot_file}")
    snapshot.dump(snapshot_file)


def profile(nframe=1, output_dir="."):
    def wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            tracemalloc.start(nframe)
            # tracemalloc.reset_peak()
            value = func(*args, **kwargs)
            take_snapshot(prefix=func.__name__, output_dir=output_dir)
            _, peak = tracemalloc.get_traced_memory()

            print(f"Peak usage: {bytes_to_gibibytes(peak):.4f} GiB")
            tracemalloc.stop()

            return value
        return _wrapped
    return wrapper


def load_profile(path):
    return tracemalloc.Snapshot.load(path)

def bytes_to_gibibytes(size: int):
    return size / (1024 * 1024 * 1024)



def summarize_snapshot(snapshot, limit=20):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<frozen importlib._bootstrap_external>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))

    by_line = snapshot.statistics("lineno")

    total = sum([line.size for line in by_line])

    print(f"Total traced memory usage {bytes_to_gibibytes(total):.4f} GiB")
    print(f"Top {limit} largest allocations.")
    for ind, stat in enumerate(by_line[:limit], 1):
        frame, *_ = stat.traceback
        print(f"#{ind}: {frame.filename}:{frame.lineno} {bytes_to_gibibytes(stat.size):.4f} GiB")
        line = linecache.getline(frame.filename, frame.lineno).strip()

    print(f"\t{line}")  
