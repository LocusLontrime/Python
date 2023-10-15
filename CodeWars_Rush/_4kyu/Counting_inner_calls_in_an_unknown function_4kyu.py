# accepted on codewars.com
import sys  # LL 36 366 98 989


def count_calls(func, *args, **kwargs):
    """Count calls in function func"""
    inner_calls = -1

    # special function for tracing the calls:
    def tracing_func(frame_type, event_str, other_args):
        nonlocal inner_calls
        if event_str == 'call':
            inner_calls += 1
        return tracing_func
    # sys tracing on:
    sys.settrace(tracing_func)
    # the value:
    rv = func(*args, **kwargs)
    # resulting tuple:
    return inner_calls, rv


def add(a, b):
    return a + b


def add_ten(x):
    return add(x, 10)


# print(f'info: {help(sys)}')

print(f'calls number: {count_calls(add, 1, 2)}')
