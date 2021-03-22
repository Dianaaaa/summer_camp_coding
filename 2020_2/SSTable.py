class SSTable:
    def __init__(self, time, pairs):
        self.time = time
        self.pairs = pairs

    def printPairs(self):
        for pair in self.pairs:
            print("("+str(pair.key)+", "+pair.value+")")
    
    def toString(self):
        result = ""
        for pair in self.pairs:
            result += "("+str(pair.key)+", "+pair.value+")\n"
        return result