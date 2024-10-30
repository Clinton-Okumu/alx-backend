#!/usr/bin/env python3
"""
class LRUCache that inherits from BaseCaching and is a caching system
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache implements LRU caching system
    """
    def __init__(self):
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item to the cache using LRU algorithm
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key = self.order[0]
            self.cache_data.pop(lru_key)
            self.order.pop(0)
            print(f"DISCARD: {lru_key}")
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
