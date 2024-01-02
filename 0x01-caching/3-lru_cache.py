#!/usr/bin/env python3
"""
LRU cache
"""

from collections import deque

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRU caching system
    """

    def __init__(self):
        """
        initialization
        """
        super().__init__()
        self.order = deque()

    def put(self, key, item):
        """
        Add item in the cache
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lru_key = self.order.pop()
                del self.cache_data[lru_key]
                print(f"DISCARD: {lru_key}")
            self.order.appendleft(key)
            self.cache_data.update({key: item})

    def get(self, key):
        """
        get item by key
        """
        if key is not None and key in self.cache_data:
            self.order.remove(key)
            self.order.appendleft(key)
            return self.cache_data[key]
        return None
