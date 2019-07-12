import time

def getFromMat(mat, x, y) :
    line = mat[y]
    count = 0
    number = ""
    for i in line : 
        if i.isdigit() :
            number += i
        else :
            count = count + int(number)
            if x <= count :
                return i
    return None
            
def matriceFromFile(fileName) :
    mapFile = open(fileName, "r")
    matrice = list()
    lines = mapFile.readlines()
    for line in lines :
       matrice.append(line)
    mapFile.close()
    return matrice


tmp1 = time.clock()
mat  = matriceFromFile("plan/file.txt")
print("Size : " , len(mat))
tmp2 = time.clock()
print(getFromMat(mat, 638, 119))

tmp3 = time.clock()
execTimeLec = tmp2 - tmp1
execTimeGet = tmp3 - tmp2

print("Temps de lecture du fichier : ", execTimeLec, "seconds")
print("Temps pour get une coord : ", execTimeGet)

