"""Dictionary with nested keys. """
from typing import Any, Sequence


class NestedKeyDictionary:
    """Dictionary with nested keys."""

    def __init__(self):
        """Initializes a `NestedKeyDictionary`."""
        self._dict = {}

    def get(self, keys: Sequence[Any]):
        """Get an item from the container.

        Args:
                keys: List of the nested keys.

        Returns:
                Value at `keys`.
        """
        data = self._dict
        for key in keys:
            data = data[key]
        return data

    def set(self, keys: Sequence[Any], value: Any):
        """Set an item into the container.

        Args:
                keys: List of the nested keys.
                value: Value to place into container.
        """
        data = self._dict
        for key in keys[:-1]:
            data = data.setdefault(key, {})
        data[keys[-1]] = value

    def pop(self, keys):
        """Remove and return (pop) a value.

        Args:
                keys: List of the nested keys.

        Returns:
                Value at `keys` that was removed.
        """
        data = self._dict
        for key in keys[:-1]:
            data = data[key]
        return data.pop(keys[-1])

    def __getitem__(self, keys):
        """Get an item from the container."""
        return self.get(keys)

    def __setitem__(self, keys, value):
        """Set an item into the container."""
        self.set(keys, value)

    def __delitem__(self, keys):
        """Delete an item from the container."""
        self.pop(keys)
