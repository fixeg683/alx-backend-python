#!/usr/bin/env python3
"""
Utility functions and decorators.
"""

def memoize(method):
    """Decorator to cache a method’s output."""
    attr_name = "_{}".format(method.__name__)

    def wrapper(self):
        # Check if cached value exists
        if not hasattr(self, attr_name):
            # Cache the result
            setattr(self, attr_name, method(self))
        # Return cached result
        return getattr(self, attr_name)

    return wrapper
