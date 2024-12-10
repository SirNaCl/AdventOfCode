from time import perf_counter_ns


def benchmark(func):
    def timed(*args, **kwargs):
        t1 = perf_counter_ns()
        res = func(*args, **kwargs)
        t2 = perf_counter_ns()
        print(f"{func.__name__} took {(t2-t1)/1000000}ms")
        return res

    return timed
