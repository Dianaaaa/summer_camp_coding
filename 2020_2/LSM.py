import struct
import KVPair
import SSTable

def inFinalState(indexs):
    for i in indexs:
        if i[0] != i[1]:
            return False
    return True

def divideKVPairs(cleanKVPairs):
    groups = []
    index = 0
    workIndex = 0
    length = 12 # meta data
    while (workIndex != len(cleanKVPairs)):
        filesize = length
        length += 8  # key & offset
        length += len(cleanKVPairs[workIndex].value) # value
        if length > 256*1024:
            groups.append([cleanKVPairs[index:workIndex], filesize])
            length = 12
            index = workIndex
        else:
            workIndex += 1
    if (index != len(cleanKVPairs)):
        groups.append([cleanKVPairs[index:workIndex], length])
    return groups
        


def loadSSTable(filepath):
    time = None
    pairs = []
    with open(filepath, "rb") as fin:
        fileSizeBytes = fin.read(4)
        timeBytes = fin.read(4)
        nKeysBytes = fin.read(4)

        time = struct.unpack('<I', timeBytes)[0]
        nKeys = struct.unpack('<I', nKeysBytes)[0]

        keyOffset = []

        for i in range(nKeys):
            keyBytes = fin.read(4)
            offsetBytes = fin.read(4)

            key = struct.unpack('<i', keyBytes)[0]
            offset = struct.unpack('<I', offsetBytes)[0]
            keyOffset.append([key, offset])
        
        for i in range(len(keyOffset)-1):
            key = keyOffset[i][0]
            offset = keyOffset[i][1]
            next_offset = keyOffset[i+1][1]

            valueLength = next_offset - offset
            valueBytes = fin.read(valueLength)
            value = valueBytes.decode()  # bytes转string

            pairs.append(KVPair.KVPair(key, value))
        lastKey = keyOffset[-1][0]
        lastValue = fin.read().decode()
        pairs.append(KVPair.KVPair(lastKey, lastValue))
        print(len(pairs), end=" ")
        print(pairs[0].key, end=" ")
        print(pairs[-1].key)
    ssTable = SSTable.SSTable(time, pairs)
    return ssTable

def sortSSTables(SSTableList):
    sortedKVPairs = []
    indexs = []
    for i in range(len(SSTableList)):
        indexs.append([0, len(SSTableList[i].pairs)])
    
    while (not inFinalState(indexs)):
        # find the first not-empty SSTable
        index = 0
        while(indexs[index][0] == indexs[index][1]): # empty
            index += 1
            # if index == len(indexs): 
            #     break

        # record the minimal kv pair
        tableIndex = index
        minPair = SSTableList[index].pairs[indexs[index][0]]
        minTime = SSTableList[index].time
        for i in range(index+1, len(SSTableList)):
            if indexs[i][0] != indexs[i][1]:
                kvPair = SSTableList[i].pairs[indexs[i][0]]
                if kvPair.key < minPair.key:
                    minPair = kvPair
                    minTime = SSTableList[i].time
                    tableIndex = i
                elif kvPair.key == minPair.key:
                    if SSTableList[i].time < minTime:
                        minPair = kvPair
                        minTime = SSTableList[i].time
                        tableIndex = i
        sortedKVPairs.append(minPair)
        indexs[tableIndex][0] += 1
    print(sortedKVPairs[0].key, end=" ")
    print(sortedKVPairs[-1].key)
    return sortedKVPairs


def cleanSSTables(sortedKVPairs):
    if (len(sortedKVPairs) == 0):
        return None
    if (len(sortedKVPairs) == 1):
        if (sortedKVPairs[0].value == ""):
            return None
        return sortedKVPairs  # no need to clean
    
    cleanKVPairs = []
    index = 0
    workIndex = 1
    while (index != len(sortedKVPairs)):
        while (workIndex != len(sortedKVPairs) and sortedKVPairs[workIndex].key == sortedKVPairs[index].key):
            workIndex += 1
        if sortedKVPairs[workIndex-1].value == "":
            index = workIndex
            workIndex += 1
        else:
            cleanKVPairs.append(sortedKVPairs[workIndex-1])
            index = workIndex
            workIndex += 1
    print(len(cleanKVPairs), end=" ")
    print(cleanKVPairs[0].key, end=" ")
    print(cleanKVPairs[-1].key)
    return cleanKVPairs
            
def saveSSTable(cleanKVPairs):
    dividedPairs = divideKVPairs(cleanKVPairs)
    for i in range(len(dividedPairs)):
        with open("./output-"+str(i+1)+".sst", "wb") as fout:
            pairs = dividedPairs[i][0]
            time = 0x00FFFFFF
            nKeys = len(pairs)
            filesize = dividedPairs[i][1]

            fout.write(struct.pack('<I', filesize))
            fout.write(struct.pack('<I', time))
            fout.write(struct.pack('<I', nKeys))
            offset = 12 + 8 * nKeys
            for j in range(nKeys):
                fout.write(struct.pack('<i', pairs[j].key))
                fout.write(struct.pack('<I', offset))
                offset += len(pairs[j].value)
            for j in range(nKeys):
                fout.write(pairs[j].value.encode())
    print(len(dividedPairs))



if __name__ == "__main__":
    table1 = loadSSTable("./small-case/sstable-1.sst")
    table2 = loadSSTable("./small-case/sstable-2.sst")
    table3 = loadSSTable("./small-case/sstable-3.sst")
    tables = [table1, table2, table3]
    sortedKVPairs = sortSSTables(tables)
    cleanKVPairs = cleanSSTables(sortedKVPairs)
    saveSSTable(cleanKVPairs)

    ans = loadSSTable("./small-case/output-2.sst")
    with open ("./ans", "w") as fin:
        fin.write(ans.toString())

    my = loadSSTable("./output-2.sst")
    with open ("./my", "w") as fin:
        fin.write(my.toString())
