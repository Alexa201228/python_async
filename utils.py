import time
from functools import wraps


def timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        res = await func(*args, **kwargs)
        res_time = time.perf_counter() - t1
        print(f'Время выполнения функции {func.__name__}: {res_time}')
        return res

    return wrapper
