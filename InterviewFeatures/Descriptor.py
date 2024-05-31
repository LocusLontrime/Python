class Descriptor:
    # def __init__(self, attr_name: str) -> None:
    #     self._attr_name = attr_name

    forbidden_attrs = {'_velocity', '_gravity'}

    def __set_name__(self, owner, attr_name: str) -> None:
        # name validation:
        if all(ch.isalpha() and not ch.isupper() or ch.isdigit() or ch == '_' for ch in attr_name):
            self._attr_name = f'_{attr_name}'
        else:
            raise ValueError(f'WRONG attr name!!! Try to use Snake case...')

    def __get__(self, instance, owner=None):
        # forbidden attrs excluded:
        if self._attr_name not in Descriptor.forbidden_attrs:
            return getattr(instance, self._attr_name)
        else:
            raise ValueError(f'{self._attr_name} attr value knowledge is strictly forbidden and therefore it cannot be shown...!!!')

    def __set__(self, instance, value: int):
        # value validation:
        if 0 <= value <= 100:
            setattr(instance, self._attr_name, value)
        else:
            raise ValueError(f'WRONG value!!! Must be 0 <= val <= 100...')

    def __delete__(self, instance) -> None:
        delattr(instance, self._attr_name)

    def __call__(self, *args, **kwargs):
        print(f'LALA!')


class Obj:
    attr_1 = Descriptor()
    speed = Descriptor()
    velocity = Descriptor()
    # try to use BlaBla name, uncomment the expression below:
    # BlaBla = Descriptor()


instance_object = Obj()

instance_object.attr_1 = 98
instance_object.velocity = 99  # try to use 989 val
instance_object.speed = 100
print(f'{instance_object.attr_1 = }')  # -> 98
del instance_object.attr_1
# print(f'{instance_object.attr_1 = }')  # error...
print(f'{instance_object.speed = }')
# print(f'{instance_object.velocity}')

print(f'{3 ** 20}')

