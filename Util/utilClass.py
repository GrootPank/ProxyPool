class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton,cls).__new__(cls,*args, **kwargs)
            return cls._instance


class LazyProperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if not instance:
            return self
        value = self.func(instance)
        setattr(instance, self.func.__name__, value)
        return value


