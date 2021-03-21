from bitarray import bitarray

def printChar(char):
    if char == "\n":
        return "\\n"
    if char == "\t":
        return "\\t"
    return char

class HuffmanTree:
    def __init__(self, char, weight, left, right):
        self.key = char
        self.weight = weight
        self.left = left
        self.right = right
    
    def getKey(self):
        return self.key
    def getWeight(self):
        return self.weight
    def getDepth(self):
        if (self.left == None and self.right == None):
            return 0
        # if (self.left == None):
        #     return self.right.getDepth() + 1
        # if (self.right == None):
        #     return self.left.getDepth() + 1
        leftDepth = self.left.getDepth()
        rightDepth = self.right.getDepth()
        return max(leftDepth, rightDepth) + 1
    def getAscii(self):
        if (self.key != None):
            return ord(self.key)
        return min(self.left.getAscii(), self.right.getAscii())
    def getCode(self, path, codeDict):
        if self.key != None:
            codeDict[self.key] = path
            return
        self.left.getCode(path+"0", codeDict)
        self.right.getCode(path+"1", codeDict)


def mergeNode(node1, node2):
    weight = node1.getWeight() + node2.getWeight()
    return HuffmanTree(None, weight, node1, node2)

def merge(forest):
    if len(forest) == 1:
        return forest
    tmp = sorted(forest, key=lambda t:t.getAscii(), reverse=False)
    sortedForest = sorted(tmp, key=lambda t:t.weight, reverse=False)
    newTree = mergeNode(sortedForest[0], sortedForest[1])
    newForest = [newTree] + sortedForest[2:]
    return newForest

def littleEndian(number):
    string = ""
    while (number != 0):
        string = str(number%2) + string
        number = number // 2
    for i in range(64-len(string)):
        string = "0" + string
    littleEndianString = ""
    for i in range(8):
        littleEndianString = string[i*8:(i+1)*8] + littleEndianString
    return littleEndianString


def do_statistics(filename):
    freqTableDict = {}
    with open(filename, "r") as fin:
        char = fin.read(1)
        while (char):
            if char in freqTableDict:
                freqTableDict[char] += 1
            else:
                freqTableDict[char] = 1
            char = fin.read(1)
    print(str(len(freqTableDict)))
    cnt = 0
    tmp = sorted(freqTableDict.items(), key=lambda d:d[0], reverse=False) # 先按ascii排序从小到大
    freqTable = sorted(tmp, key=lambda d:d[1], reverse=True) # 再按freq排序从大到小
    for i in freqTable:
        if cnt == 3:
            break
        print(printChar(i[0])+","+str(i[1]))
        cnt += 1

    return freqTable # list

def build_tree(freqTable):
    forest = []
    for i in freqTable:
        forest.append(HuffmanTree(i[0], i[1], None, None))
    while (len(forest) != 1):
        forest = merge(forest)
    print(str(forest[0].getDepth()))
    huffmanTree = forest[0]
    return huffmanTree

def encode(tree, filename):
    if (tree.key != None):
        return
    codingTable = {}
    tree.getCode("", codingTable)

    sortedCT = sorted(codingTable.items(), key=lambda i:i[0], reverse=False) # 按ascii排序从小到大
    with open("./output/"+filename+".huffidx", "w") as fout:
        for i in sortedCT:
            fout.write(i[0]+" "+i[1]+"\n")
    print(codingTable["e"])
    return codingTable

def compress(filepath, codingTable, filename):
    with open(filepath, "r") as fin, open("./output/"+filename+".huffzip", "wb") as fout:
        char = fin.read(1)
        validBitCnt = 0
        fileString = ""
        while (char):
            code = codingTable[char]
            validBitCnt += len(code)
            fileString += code
            char = fin.read(1)
        if validBitCnt % 8 != 0:
            for i in range(8-(validBitCnt%8)):
                fileString += "0"
        print(validBitCnt)
        littleEndianString = littleEndian(validBitCnt)
        fout.write(bitarray(littleEndianString))
        fout.write(bitarray(fileString))


if __name__ == "__main__":
    freqTable = do_statistics("./input/small.txt")
    huffmanTree = build_tree(freqTable)
    codingTable = encode(huffmanTree, "my_small")
    compress("./input/small.txt", codingTable, "my_small")



            