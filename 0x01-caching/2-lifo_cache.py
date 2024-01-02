#!/usr/bin/env python3
"""LIFO Caching"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """caching system"""

    def put(self, key, item):
        """Add new item"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = list(self.cache_data.keys())[-1]
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")

            self.cache_data.update({key: item})

    def get(self, key):
        """Get item by key"""
        return self.cache_data.get(key)
