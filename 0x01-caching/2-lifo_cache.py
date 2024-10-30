#!/usr/bin/env python3
"""
This module implements a LIFO (Last-In-First-Out) caching system
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache implements LIFO caching system
    """

    def __init__(self):
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item to the cache using LIFO algorithm
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
                return
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                last_key = self.order[-1]
                self.cache_data.pop(last_key)
                self.order.pop()
                print(f"DISCARD: {last_key}")
            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """
        Retrieve an item from cache
        """
        if key is not None:
            return self.cache_data.get(key)
        return None
