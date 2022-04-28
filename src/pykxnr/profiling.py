import pickle
import tracemalloc
import os
import datetime
from functools import wraps


def profile(nframe=1, output_dir="."):
    abspath = os.path.abspath(output_dir)
    os.makedirs(abspath, exist_ok=True)

    def wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            tracemalloc.start(nframe)
            value = func(*args, **kwargs)
            snapshot = tracemalloc.take_snapshot()
            
            snapshot_file = os.path.join(abspath, f"{func.__name__}_{datetime.datetime.now().isoformat()}.pkl")
            print(f"Saving memory usage snapshot to: {snapshot_file}")

            with open(snapshot_file, 'wb') as f:
                pickle.dump(snapshot, f)

            tracemalloc.stop()

            return value
        return _wrapped
    return wrapper


def load_profile(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


