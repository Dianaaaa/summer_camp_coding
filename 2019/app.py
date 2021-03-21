import LinearHash
import CuckooHash


#hashmap = LinearHash.LinearHash(8)
hashmap = CuckooHash.CuckooHash(8)

# read data
with open("./small.in", "r") as fin, open("./my_small.ans", "w") as fout:
    while True:
        line  = fin.readline()
        if (not line):
            break
        
        a = line.split(" ")
        if a[0] == "Set":
            key = int(a[1])
            value = int(a[2])
            hashmap.insert(key, value)


        if a[0] == "Get":
            key = int(a[1])
            result = hashmap.lookup(key)
            if (result == None):
                fout.write("null\n")
            else:
                fout.write(str(result) + "\n")


        if a[0] == "Del":
            key = int(a[1])
            hashmap.delete(key)