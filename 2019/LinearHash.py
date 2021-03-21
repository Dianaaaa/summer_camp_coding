# !/usr/bin/python3
# coding=utf8

import copy
from Pair import *

class LinearHash:
    def __init__(self, cap):
        self.capacity = cap
        self.hash_table = []
        self.cnt = 0
        for i in range(cap):
            self.hash_table.append(Pair(-1, -1))

    def expand(self):
        old_cap = self.capacity
        old_htb = copy.deepcopy(self.hash_table)
        self.capacity *= 2
        self.hash_table = []
        self.cnt = 0
        for i in range(self.capacity):
            self.hash_table.append(Pair(-1, -1))
        for i in range(0, old_cap):
            if (old_htb[i].getKey() != 0):
                self.insert(old_htb[i].getKey(), old_htb[i].getValue())

    def lookup(self, key):
        index = hash(key, self.capacity)
        for i in range(index,self.capacity):
            if self.hash_table[i].getKey() == key:
                return self.hash_table[i].getValue()
            if self.hash_table[i].getKey() == -1:
                return None
        for i in range(0, index):
            if self.hash_table[i].getKey() == key:
                return self.hash_table[i].getValue()
            if self.hash_table[i].getKey() == -1:
                return None
        return None


    def insert(self, key, value):
        index = hash(key, self.capacity)
        for i in range(index, self.capacity):
            if (self.hash_table[i].getKey() == -1):
                self.hash_table[i] = Pair(key, value)
                self.cnt += 1
                if (self.cnt > (self.capacity / 2)):
                    self.expand()
                return
            if (self.hash_table[i].getKey() == key):
                self.hash_table[i] = Pair(key, value)
                return
        for i in range(0, index):
            if (self.hash_table[i].getKey() == -1):
                self.hash_table[i] = Pair(key, value)
                self.cnt += 1
                if (self.cnt > (self.capacity / 2)):
                    self.expand()
                return
            if (self.hash_table[i].getKey() == key):
                self.hash_table[i] = Pair(key, value)
                return
        
    def delete(self, key):
        index = hash(key, self.capacity)
        for i in range(index, self.capacity):
            if self.hash_table[i].getKey() == -1:
                return
            if self.hash_table[i].getKey() == key:
                self.hash_table[i] = Pair(-1, -1)
                empty_index = i
                for j in range(i+1, self.capacity):
                    if (self.hash_table[j].getKey() == -1):
                        continue
                    elif (hash(self.hash_table[j].getKey(), self.capacity) <= empty_index and hash(self.hash_table[j].getKey(), self.capacity) > j):
                        self.hash_table[empty_index] = self.hash_table[j]
                        self.hash_table[j] = Pair(-1, -1)
                        empty_index = j
                for j in range(0, i):
                    if (self.hash_table[j].getKey() == -1):
                        continue
                    elif (hash(self.hash_table[j].getKey(), self.capacity) <= empty_index and hash(self.hash_table[j].getKey(), self.capacity) > j):
                        self.hash_table[empty_index] = self.hash_table[j]
                        self.hash_table[j] = Pair(-1, -1)
                        empty_index = j
                

            
            


    