import LinearHash
import CuckooHash
import random
import time

import matplotlib.pyplot as plt
import numpy as np

# initiate
linearHashMap = LinearHash.LinearHash(8)
cuckooHashMap = CuckooHash.CuckooHash(8)
uperbound = 2000
interval = 1

# data
linearInitTime = []
cuckooInitTime = []
linearGetTime = []
cuckooGetTime = []
linearGetSetTime = []
cuckooGetSetTime = []
linearGetCnt = 0
cuckooGetCnt = 0
linearGetSetCnt = 0
cuckooGetSetCnt = 0


for i in range(0, 1000):
    randKey = random.randint(0, uperbound)
    randValue = random.randint(0, uperbound)
    t1 = time.time()
    linearHashMap.insert(randKey, randValue)
    t2 = time.time()
    t = t2 - t1
    linearInitTime.append(t*1000)

    t1 = time.time()
    cuckooHashMap.insert(randKey, randValue)
    t2 = time.time()
    t = t2 - t1
    cuckooInitTime.append(t*1000)

print("insert end\n")

timeout = time.time() + interval
while True:
    if time.time() > timeout:
        break
    randKey = random.randint(0, uperbound)
    t1 = time.time()
    linearHashMap.lookup(randKey)
    t2 = time.time()
    t = t2 - t1
    linearGetCnt += 1
    linearGetTime.append(t*1000)
        
timeout = time.time() + interval
while True:
    if time.time() > timeout:
        break
    randKey = random.randint(0, uperbound)
    t1 = time.time()
    cuckooHashMap.lookup(randKey)
    t2 = time.time()
    t = t2 - t1
    cuckooGetSetCnt += 1
    cuckooGetTime.append(t*1000)

print("get ended\n")

timeout = time.time() + interval
while True:
    if time.time() > timeout:
        break
    randKey = random.randint(0, uperbound)
    randValue = random.randint(0, uperbound)
    t1 = time.time()
    linearHashMap.insert(randKey, randValue)
    t2 = time.time()
    randKey = random.randint(0, uperbound)
    t3 = time.time()
    linearHashMap.lookup(randKey)
    t4 = time.time()
    linearGetSetTime.append((t2-t1)*1000)
    linearGetSetTime.append((t4-t3)*1000)
    linearGetSetCnt += 2

timeout = time.time() + interval
while True:
    if time.time() > timeout:
        break
    randKey = random.randint(0, uperbound)
    randValue = random.randint(0, uperbound)
    t1 = time.time()
    cuckooHashMap.insert(randKey, randValue)
    t2 = time.time()
    randKey = random.randint(0, uperbound)
    t3 = time.time()
    cuckooHashMap.lookup(randKey)
    t4 = time.time()
    cuckooGetSetTime.append((t2-t1)*1000)
    cuckooGetSetTime.append((t4-t3)*1000)
    cuckooGetSetCnt += 2

print("all ended\n")

# draw
# 1 init time delay
ax1 = plt.subplot(1, 2, 1)
x = [i for i in range(0, 1000)]
plt.plot(x, linearInitTime)

ax2 = plt.subplot(1, 2, 2)
plt.plot(x, cuckooInitTime)

plt.tight_layout()
plt.savefig('line-chart-v3.pdf', dpi=300)
plt.show()


