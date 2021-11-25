def add_command(*args, **kwargs):
    def decorator(func):
        command_name = kwargs["command"]
        args[0][command_name] = func

    return decorator
