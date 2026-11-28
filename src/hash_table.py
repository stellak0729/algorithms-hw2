"""A string-keyed hash table using separate chaining."""

from __future__ import annotations


class _Node:
    __slots__ = ("key", "value", "next")

    def __init__(self, key: str, value: str, next_node: _Node | None = None):
        self.key = key
        self.value = value
        self.next = next_node


class HashTable:
    def __init__(self, initial_capacity: int = 8):
        if (
            not isinstance(initial_capacity, int)
            or isinstance(initial_capacity, bool)
        ):
            raise TypeError("initial_capacity must be an integer")
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be positive")

        self.capacity = initial_capacity
        self._buckets: list[_Node | None] = [None] * self.capacity
        self._size = 0

    def _index(self, key: str) -> int:
        index = 0
        for character in key:
            index = (index * 31 + ord(character)) % self.capacity
        return index

    def put(self, key: str, value: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if not isinstance(value, str):
            raise TypeError("value must be a string")

        index = self._index(key)
        node = self._buckets[index]
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        self._buckets[index] = _Node(key, value, self._buckets[index])
        self._size += 1
        if self._size / self.capacity > 0.75:
            self._resize()

    def get(self, key: str) -> str | None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")

        node = self._buckets[self._index(key)]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def _resize(self) -> None:
        old_buckets = self._buckets
        self.capacity *= 2
        self._buckets = [None] * self.capacity

        for bucket in old_buckets:
            node = bucket
            while node is not None:
                index = self._index(node.key)
                self._buckets[index] = _Node(
                    node.key,
                    node.value,
                    self._buckets[index],
                )
                node = node.next
