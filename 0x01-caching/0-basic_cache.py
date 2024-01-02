#!/usr/bin/env python3
"""Basic Cache"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """cashing system"""

    def put(self, key, item):
        """Add an item to the cache"""
        if key is not None and item is not None:
            self.cache_data.update({key: item})

    def get(self, key):
        """Get in item by the key"""
        return self.cache_data.get(key)
