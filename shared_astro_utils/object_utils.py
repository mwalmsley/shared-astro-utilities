
def object_to_dict(obj):
    excluded_keys = ['__dict__', '__doc__', '__module__', '__weakref__']
    # TODO use dict comprehension
    return dict(
        [(key, value) for (key, value) in obj.__dict__.items() if key not in excluded_keys]
        )
