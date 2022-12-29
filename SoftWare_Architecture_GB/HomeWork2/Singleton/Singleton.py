def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance



@singleton
class MyClass:
    pass


c1 = MyClass()
c2 = MyClass()

if id(c1) == id(c2):
    print(f'Singleton works fine!')
else:
    print(f'Singleton concept been failed...')