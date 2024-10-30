#!/usr/bin/env python3
"""
This module implements a MRU (Most Recently Used) caching system
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache implements MRU caching system
    """

    def __init__(self):
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item to the cache using MRU algorithm
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                mru_key = self.order[-1]
                self.cache_data.pop(mru_key)
                self.order.pop()
                print(f"DISCARD: {mru_key}")
            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """
        Retrieve an item from cache
        """
        if key is not None and key in self.cache_data:
            self.order.remove(key)
            self.order.append(key)
            return self.cache_data.get(key)
        return None
