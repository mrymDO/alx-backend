#!/usr/bin/env python3
"""MRU Caching"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRU Caching"""

    def __init__(self):
        """initialization"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """add item in the cache"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                mru_key = self.order.pop()
                del self.cache_data[mru_key]
                print(f"DISCARD: {mru_key}")

            self.order.append(key)
            self.cache_data.update({key: item})

    def get(self, key):
        """retrieve item by key"""
        if key is not None and key in self.cache_data:
            self.order.remove(key)
            self.order.append(key)
            return self.cache_data.get(key)
        return None
