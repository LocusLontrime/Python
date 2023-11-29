# accepted on codewars.com
import operator


def zero(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def one(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def two(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def three(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def four(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def five(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def six(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def seven(*args):
    print(f'args: {args}')
    return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def eight(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def nine(*args): return 0 if len(args) == 0 else args[0](0, args[1])  # your code here


def plus(f): return operator.add, f  # your code here


def minus(f): return operator.sub, f  # your code here


def times(f): return operator.mul, f  # your code here


def divided_by(f): return operator.floordiv, f  # your code here


seven(times(five()))


