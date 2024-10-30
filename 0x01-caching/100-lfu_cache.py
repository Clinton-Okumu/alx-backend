#!/usr/bin/env python3
"""
This module implements a LFU (Least Frequently Used) caching system
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache implements LFU caching system
    """

    def __init__(self):
        super().__init__()
        self.freq = {}      # Track frequency of each key
        self.order = []     # Track order of use for LRU tiebreaker
        self.freq_lists = {}  # Group keys by frequency

    def put(self, key, item):
        """
        Add an item to the cache using LFU algorithm
        """
        if key is not None and item is not None:
            # Update existing key
            if key in self.cache_data:
                self.cache_data[key] = item
                self.update_frequency(key)
                return

            # Handle cache full condition
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self.remove_least_frequent()

            # Add new item
            self.cache_data[key] = item
            self.freq[key] = 1
            self.order.append(key)
            if 1 not in self.freq_lists:
                self.freq_lists[1] = []
            self.freq_lists[1].append(key)

    def get(self, key):
        """
        Retrieve an item from cache
        """
        if key is not None and key in self.cache_data:
            self.update_frequency(key)
            return self.cache_data[key]
        return None

    def update_frequency(self, key):
        """
        Update frequency and order for a key
        """
        current_freq = self.freq[key]
        self.freq[key] = current_freq + 1
        new_freq = current_freq + 1

        # Remove from current frequency list
        self.freq_lists[current_freq].remove(key)
        if not self.freq_lists[current_freq]:
            del self.freq_lists[current_freq]

        # Add to new frequency list
        if new_freq not in self.freq_lists:
            self.freq_lists[new_freq] = []
        self.freq_lists[new_freq].append(key)

        # Update order for LRU
        self.order.remove(key)
        self.order.append(key)

    def remove_least_frequent(self):
        """
        Remove the least frequently used item
        If tie, remove least recently used among least frequent
        """
        # Find minimum frequency
        min_freq = min(self.freq_lists.keys())

        # Get least recently used among items with min frequency
        lfu_items = self.freq_lists[min_freq]
        for item in self.order:
            if item in lfu_items:
                lfu_key = item
                break

        # Remove the item
        self.cache_data.pop(lfu_key)
        self.freq.pop(lfu_key)
        self.order.remove(lfu_key)
        self.freq_lists[min_freq].remove(lfu_key)
        if not self.freq_lists[min_freq]:
            del self.freq_lists[min_freq]
        print(f"DISCARD: {lfu_key}")
