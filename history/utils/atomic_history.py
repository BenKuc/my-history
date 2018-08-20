# TODO: create a decorator/context-manager that puts everything inside in one history event!
from contextlib import ContextDecorator


class Atomic(ContextDecorator):

    def __init__(self):
        # TODO: which arguments does it need?
        # TODO: initialize variables needed
        pass

    # TODO: look into context-manager to see how to implement enter and exit
    # TODO: ideas for implementation:
    #       1) connect internal method (or dispatcher?) to all the signals
    #       2) this signal leads to not activating the other signals
    #           (maybe by disconnecting them temporarily)
    #       3) disconnect dispatcher and connect others again

    # TODO: implement
    def __enter__(self):
        pass

    # TODO: implement
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
