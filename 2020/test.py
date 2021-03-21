with open("./input/small.huffidx") as fin1, open("./output/my_small.huffidx") as fin2:
    count = 0
    

    while True:
        line1 = fin1.readline()
        line2 = fin2.readline()
        if (line1 and line2):
            count += 1
            if (line1 != line2):
                print("line "+str(count)+"\n")
                break
        else:
            break
