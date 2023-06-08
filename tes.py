x= "Hahaha.txt"
indexType=0
for i in x[::-1]:
    if i == ".":
        break
    indexType += 1
print (x[0:len(x)-indexType-1])