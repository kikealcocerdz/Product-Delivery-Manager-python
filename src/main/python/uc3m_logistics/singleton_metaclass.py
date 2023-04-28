# pylint: disable=missing-module-docstring
class SingletonMeta(type):
    """Abstract class for creating singleton"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
