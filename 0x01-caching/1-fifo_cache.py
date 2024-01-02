#!/usr/bin/env python3
"""FIFO caching"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Caching system"""

    def put(self, key, item):
        """Add a new item"""
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discarded_key = next(iter(self.cache_data))
            del self.cache_data[discarded_key]
            print(f"DISCARD: {discarded_key}")

        self.cache_data.update({key: item})

    def get(self, key):
        """get item by key"""
        return self.cache_data.get(key)
