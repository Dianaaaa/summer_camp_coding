from Pair import *
from copy import deepcopy

class CuckooHash:
    def __init__(self, cap):
        self.capacity = cap
        self.htb1 = []
        self.htb2 = []
        for i in range(self.capacity):
            self.htb1.append(Pair(-1, -1))
            self.htb2.append(Pair(-1, -1))
        
    def expand(self):
        old_cap = self.capacity
        old_htb1 = deepcopy(self.htb1)
        old_htb2 = deepcopy(self.htb2)
        self.capacity *= 2
        self.htb1 = []
        self.htb2 = []
        for i in range(self.capacity):
            self.htb1.append(Pair(-1, -1))
            self.htb2.append(Pair(-1, -1))
        
        for i in range(0, old_cap):
            if (old_htb1[i].getKey() != -1):
                self.insert(old_htb1[i].getKey(), old_htb1[i].getValue())
            if (old_htb2[i].getKey() != -1):
                self.insert(old_htb2[i].getKey(), old_htb2[i].getValue())
    
    def lookup(self, key):
        index1 = hash(key, self.capacity)
        index2 = hash2(key, self.capacity)
        if (self.htb1[index1].getKey() == key):
            return self.htb1[index1].getValue()
        if (self.htb2[index2].getKey() == key):
            return self.htb2[index2].getValue()
        return None


    def insert(self, key, value):
        move1 = []
        move2 = []
        cap = self.capacity
        new_htb1 = deepcopy(self.htb1)
        new_htb2 = deepcopy(self.htb2)
        cur_pair = Pair(key, value)
        while True:
            index1 = hash(cur_pair.getKey(), cap)
            if (new_htb1[index1].getKey() == cur_pair.getKey() or self.htb1[index1].getKey() == -1):
                new_htb1[index1] = cur_pair
                self.htb1 = new_htb1
                self.htb2 = new_htb2
                return   # successfully inserted in htb1
            if index1 in move1:  # circle: need expanding and re-insert
                self.expand()
                self.insert(key, value)
                return
            move1.append(index1)
            tmp = new_htb1[index1]
            new_htb1[index1] = cur_pair
            cur_pair = tmp

            index2 = hash2(cur_pair.getKey(), cap)
            if (new_htb2[index2].getKey() == cur_pair.getKey() or self.htb2[index2].getKey() == -1):
                new_htb2[index2] = cur_pair
                self.htb1 = new_htb1
                self.htb2 = new_htb2
                return   # successfully inserted in htb2
            if index2 in move2:  # circle: need expanding and re-insert
                self.expand()
                self.insert(key, value)
                return
            move2.append(index2)
            tmp = new_htb2[index2]
            new_htb2[index2] = cur_pair
            cur_pair = tmp

    def delete(self, key):
        index1 = hash(key, self.capacity)
        index2 = hash2(key, self.capacity)
        if (self.htb1[index1].getKey() == key):
            self.htb1[index1] = Pair(-1, -1)
        if (self.htb2[index2].getKey() == key):
            self.htb2[index2] = Pair(-1, -1)

            