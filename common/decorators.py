from time import perf_counter_ns
from pprint import pprint


def benchmark(func):
    def timed(*args, **kwargs):
        t1 = perf_counter_ns()
        res = func(*args, **kwargs)
        t2 = perf_counter_ns()
        print(f"{func.__name__} took {(t2-t1)/1000000}ms")
        return res

    return timed


def debug(func):
    def printres(*args, **kwargs):
        res = func(*args, **kwargs)
        sep = "," if len(args) > 0 and len(kwargs) > 0 else ""
        astr = ",".join(list(map(str, args)))
        kstr = (
            ",".join(f"{k}={v}" for k, v in kwargs.items()) if len(kwargs) > 0 else ""
        )
        print(f"{func.__name__}({astr}{sep}{kstr}): ", end="")
        pprint(res)
        return res

    return printres
