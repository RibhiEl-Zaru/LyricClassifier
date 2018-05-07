
numLinesForGenre = [] #Used for calculating buckets for freqDist keys
allLineNums = []
minimumLines = float("inf")
maximumLines = -float("inf")



def initializeNumLinesForGenere(GENRES):
    global numLinesForGenre
    numLinesForGenre = [[] for i in range(len(GENRES))] #Used for calculating buckets for freqDist keys

def addLineNum(numLines):
    global minimumLines
    global maximumLines

    allLineNums.append(numLines)

    if(numLines < minimumLines):
        minimumLines = numLines
    if(numLines > maximumLines):
        maximumLines = numLines


def bucketizeScore(score):
    print(maximumLines)
    print(minimumLines)
    numer = score - minimumLines

    denom = maximumLines - minimumLines
    print(numer)
    print(denom)
    print(score)
    score = numer/denom
    return score

def addLinesForGenre(numLines, index):
    numLinesForGenre[index].append(numLines)


def getAllLineNums():
    return allLineNums

def getNumLinesForGenre():
    return numLinesForGenre
