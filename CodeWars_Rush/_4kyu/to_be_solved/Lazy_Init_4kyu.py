# accepted on codewars.com
import inspect


# the metaclass to be used
class LazyInit(type):
    @classmethod
    def lazy(cls, init_func):
        def wrapper(*args):
            params = inspect.getfullargspec(init_func).args
            self = args[0]

            for ind in range(1, len(params)):
                setattr(self, params[ind], args[ind])

        return wrapper

    def __new__(cls, class_name, bases, attrs):
        _class = type(class_name, bases, attrs)
        setattr(_class, '__init__', LazyInit.lazy(attrs['__init__']))
        return _class


class Person(metaclass=LazyInit):
    def __init__(self, name, age): pass


# When we create a Person object like:
a_person = Person('John', 25)

# The expected behavior will be:
print(a_person.name)  # this will print John
print(a_person.age)  # this will print 25
