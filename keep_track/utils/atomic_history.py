from contextlib import ContextDecorator
# TODO L


class Atomic(ContextDecorator):

    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def atomic_history(func=None):
    # Bare decorator: @atomic -- although the first argument is called
    # `using`, it's actually the function being decorated.
    if callable(func):
        return Atomic()(func)
    # Decorator: @atomic(...) or context manager: with atomic(...): ...
    else:
        return Atomic()
