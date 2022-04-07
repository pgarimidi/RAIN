import numpy as np
import random as rd

labelings = 0
totalData = []

def genHyperplane(d, numPoints,noise,bounds):
    coefficients = []
    for i in range(d+1):
        c = rd.randint(-7,7)
        coefficients.append(c)


    points = []

    for i in range(numPoints):
        point = []
        for i in range(d):
            x = rd.random()*(bounds[i][1] - bounds[i][0]) +bounds[i][0]
            point.append(x)
        point.append(1)

        if np.dot(point,coefficients) < 0:
            label = 0
        else:
            label = 1

        corruption = rd.random()
        if corruption < noise:
            label  = 1-label

        points.append([point,label])

    return (points,coefficients)

def fillVersionSpace(cur,d,bound):
    if len(cur) == 0:
        for i in range(-bound,bound+1):
            cur.append([i])
    if len(cur[0]) == d+1:
        return cur

    v = []
    for c in cur:
        for i in range(-bound,bound+1):
                temp = c.copy()
                temp.append(i)
                v.append(temp)
    return fillVersionSpace(v,d,bound)

def sampleBox(bounds):
    box = []
    for i in range(len(bounds)):
        x = rd.random()*(bounds[i][1]-bounds[i][0])+bounds[i][0]
        y = rd.random()*(bounds[i][1]-bounds[i][0])+bounds[i][0]

        boxBound = []
        boxBound.append(min(x,y))
        boxBound.append(max(x,y))
        box.append(boxBound)
    return box

def getPoints(box,points):
    boxPoints = []
    d = len(box)
    for p in points:
        inBox = True
        for i in range(d):
             if p[0][i] > box[i][1] or p[0][i] < box[i][0]:
                 inBox = False
                 break
        if inBox:
            boxPoints.append(p)
    return boxPoints

def evalBox(boxPoints,trueV,versionSpace):
    global labelings
    total = len(boxPoints)
    count0 = []
    for v in versionSpace:
        count = 0
        for p in boxPoints:
            if np.dot(p[0],v) < 0:
                count += 1
        count0.append(count)

    cMin = total
    cMax = 0
    for c in count0:
        if c < cMin:
            cMin = c
        if c > cMax:
            cMax = c
    if cMax - cMin > 2:
        labelings += 1
        trueCount = 0
        for p in boxPoints:
            if np.dot(p[0],trueV) < 0 :
                trueCount += 1
        versionSpace = [versionSpace[i] for i in range(len(versionSpace)) if abs(count0[i]-trueCount) < max(2,len(boxPoints)*.01)]

    return versionSpace

def cleanVersionSpace(points,versionSpace):
    labels = []
    for v in versionSpace:
        vLabel = []
        for p in points:
            if np.dot(p[0],v) < 0:
                l = 0
            else:
                l = 1
            vLabel.append(l)
        labels.append(vLabel)

    same = []

    for i in range(len(versionSpace)):
        for j in range(i+1,len(versionSpace)):
            if labels[j] == labels[i]:
                same.append(j)

    versionSpace = [versionSpace[i] for i in range(len(versionSpace)) if i not in same]
    return versionSpace

def testingChanges()
    print("yay")

def testAlg(d, numPoints, noise, bounds,i):
    global totalData, labelings
    versionHistory = [[3375,0]]
    points,trueV = genHyperplane(d,numPoints,noise,bounds)
    versionSpace = fillVersionSpace([],d,7)
    #cleanVersionSpace(points,versionSpace)
    #print(len(versionSpace))
    boxes = 0
    labelings = 0
    while(len(versionSpace) > 1):
        boxes += 1
        if boxes == 25:
            versionSpace = cleanVersionSpace(points,versionSpace)
        box = sampleBox(bounds)
        boxPoints = getPoints(box,points)
        versionSpace = evalBox(boxPoints,trueV,versionSpace)
        versionHistory.append([len(versionSpace),labelings])
        #print(f"Num Queries:{boxes}")
        #print(f"Size of Version Space: {len(versionSpace)}")
        if boxes == 10000:
            break
    np.savetxt(f"d=3,b=.01,{i}.csv", versionHistory,fmt='%4g', delimiter=",")
    print("--------------------------")
    print(f"True Hyperplane {trueV}")
    print(f"Predicted Hyperplane {versionSpace[0]}")
    print(f"Total Queried Boxes:{boxes}")
    print(f"Total Times Asked for Labelings {labelings}")
    totalData.append([boxes,labelings])

def main():
    d=3
    bounds = []
    for i in range(d):
        bounds.append([-20,20])

    numPoints = 10000
    noise = 0

    # points,trueV = genHyperplane(d,numPoints,noise,bounds)
    # versionSpace = fillVersionSpace([],d,7)
    # versionSpace = cleanVersionSpace(points,versionSpace)
    # np.savetxt("d=2 Hyperplanes", versionSpace , fmt = '%2g', delimiter = ",")
    # print("done")

    for i in range(15):
        testAlg(d,numPoints,noise,bounds,i)

    totalBoxes = 0
    totalLabelings = 0
    for i in range(15):
        totalBoxes += totalData[i][0]
        totalLabelings += totalData[i][1]

    print(totalBoxes/25)
    print(totalLabelings/25)


    np.savetxt("d=3,b=.01.csv", totalData,fmt='%4g', delimiter=",")

main()
