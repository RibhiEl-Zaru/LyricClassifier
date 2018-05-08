import math

numLinesForGenre = None #Used for calculating buckets for freqDist keys. Becomes a list of lists where ith list is list of numLines per genre
allLineNums = []
minimumLines = float("inf")
maximumLines = -float("inf")
freqMaps = None
bucketNum = 10

def generateFrequencyMap():
    numGenres = len(numLinesForGenre)
    totalNumLines = [0 for i in range(numGenres)]


    '''
    Initialize frequency count for the genres
    '''
    for i in  range(numGenres):

        genreList = numLinesForGenre[i]
        currFreqMap = freqMaps[i]
        for score in genreList:
            bucketizedScore = bucketizeScore(score)
            try:
                currFreqMap[bucketizedScore] += 1
            except:
                currFreqMap[bucketizedScore] = 1
            totalNumLines[i] += score


    '''
    Process the freqency distributions for each word
    '''

    for i in range(numGenres):
        freqDist = freqMaps[i]

        for key in freqDist:
            freqDist[key] = math.log(freqDist[key]) - math.log(totalNumLines[i])

    return freqMaps


def initialize(GENRES, newBucket):
    global numLinesForGenre
    global bucketNum
    global freqMaps

    bucketNum = newBucket
    numLinesForGenre = [[] for i in range(len(GENRES))] #Used for calculating buckets for freqDist keys
    freqMaps = [{} for i in range(len(GENRES))]

def addLineNum(numLines):
    global minimumLines
    global maximumLines

    allLineNums.append(numLines)

    if(numLines < minimumLines):
        minimumLines = numLines
    if(numLines > maximumLines):
        maximumLines = numLines


def bucketizeScore(score):
    numer = score - minimumLines

    denom = maximumLines - minimumLines

    score = numer/denom
    bucketScore = int(score * bucketNum)
    if score==1:
        bucketScore = bucketNum-1
    return bucketScore

def addLinesForGenre(numLines, index):
    numLinesForGenre[index].append(numLines)


def getAllLineNums():
    return allLineNums

def getNumLinesForGenre():
    return numLinesForGenre
