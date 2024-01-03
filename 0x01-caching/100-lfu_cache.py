#!/usr/bin/env python3
""" LFU caching"""

from collections import defaultdict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFU caching"""

    def __init__(self):
        """initialization"""
        super().__init__()
        self.frequency = defaultdict(int)

    def put(self, key, item):
        """Add or update an item in the cache"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self._discard_lfu()

            self.cache_data.update({key: item})
            self.frequency[key] += 1

    def get(self, key):
        """retrieve item by key"""
        if key is not None and key in self.cache_data:
            self.frequency[key] += 1
            return self.cache_data[key]
        return None

    def _discard_lfu(self):
        """discard lfu"""
        min_freq = min(self.frequency.values())
        lfu_keys = [
                key
                for key, freq in self.frequency.items()
                if freq == min_freq
        ]

        if len(lfu_keys) == 1:
            discarded_key = lfu_keys[0]
        else:
            discarded_key = min(lfu_keys, key=lambda k: self.frequency[k])

        del self.cache_data[discarded_key]
        del self.frequency[discarded_key]
        print(f"DISCARD: {discarded_key}")
