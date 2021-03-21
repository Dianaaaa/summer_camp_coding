def hash(x, cap):
    return x % cap

def hash2(x, cap):
    return (x // cap) % cap


class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    def getKey(self):
        return self.key
    
    def getValue(self):
        return self.value