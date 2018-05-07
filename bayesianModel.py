import math


truePosKey = "truePos"
trueNegKey = "trueNeg"
falsePosKey = "falsePos"
falseNegKey = "falseNeg"
numIterationsKey = "numIters"
import ngram_FreqDist

confMatrix = {}
## FUNCTION USING NAIVE BAYES PROBS TO PREDICT SENTIMENT

def naiveBayesWithFeatures(featureMap, genreList, freqMaps):

    defaultprob = math.log(0.0000000000001)
    scores = [0 for i in range(len(genreList))]
    toRet = None
    highScore = -float("inf")
    reviewwords = featureMap["reviewwords"]
    numVerses = featureMap["numVerses"]

    ngramFreqDists = freqMaps["ngramFreqDists"]
    numVersesFreqDists = freqMaps["numVersesFreqDists"]

    reviewWordLen = len(reviewwords)

    for i in range(len(genreList)):
        ngramFreqDist = ngramFreqDists[i]
        numVersesFreqDist = numVersesFreqDists[i]
        score = ngramFreqDist.get(reviewwords[0], defaultprob)
        for j in range(1, reviewWordLen):
            score += ngramFreqDist.get(reviewwords[j], defaultprob)

        score += numVersesFreqDist.get(numVerses, defaultprob)*reviewWordLen

        if score > highScore:
            highScore = score
            toRet = genreList[i]

    return toRet

def naive_bayes(freqMap, genreList, freqMaps):
    defaultprob = math.log(0.0000000000001)
    scores = [0 for i in range(len(genreList))]

    toRet = None
    highScore = -float("inf")

    reviewwords = freqMap["reviewwords"]

    ngramFreqDists = freqMaps["ngramFreqDists"]
    for i in range(len(genreList)):
        freqDist = ngramFreqDists[i]
        score = freqDist.get(reviewwords[0], defaultprob)
        for j in range(1, len(reviewwords)):
            score += freqDist.get(reviewwords[j], defaultprob)

        if score > highScore:
            highScore = score
            toRet = genreList[i]

    return toRet

def naiveBayesSentimentAnalysis(testData, genreList, freqDistLists, ngramLen):



    confusionMatrix =  [[0 for i in range(len(genreList))]for i in range(len(genreList))]

    numCorrect = 0
    guesses = [0 for i in range(len(genreList))]
    correctGuesses = [0 for i in range(len(genreList))]
    actual =  [0 for i in range(len(genreList))]

    for song in testData:
        if(len(song.lyrics)<ngramLen):
            continue;

        reviewWords = ngram_FreqDist.ngrams(song.lyrics, ngramLen)

        positives = song.genres

        featureMap = {}
        featureMap["reviewwords"] = reviewWords
        featureMap["numVerses"] = song.numVerses

        result = naiveBayesWithFeatures(featureMap, genreList, freqDistLists)

        guesses[genreList.index(result)] += 1
        c = genreList.index(result)
        for genre in positives:
            r = genreList.index(genre)
            confusionMatrix[r][c]+= 1

        for genre in positives:
            if genre == result:
                numCorrect += 1
                correctGuesses[genreList.index(result)] += 1
            actual[genreList.index(genre)] += 1
    accuracy = numCorrect/len(testData)
    x = analyzeConfusionMatrix(confusionMatrix, genreList)
    #displayPerformanceInterpretation(x)

    #for row in range(len(confusionMatrix[0])):
        #print(confusionMatrix[row])
    '''
    print("Genres\t", genreList)
    print("Guesses\t", guesses)
    print("Correct Guesses\t", correctGuesses)
    print("Actual Data\t", actual)
    print("Percentage Correct for Genre\t", [round(correctGuesses[i]/actual[i],4) for i in range(len(actual))])
    print("ACCURACY:\t", accuracy)
    '''
    return accuracy


def displayPerformanceInterpretation(genreResultsMap, GENRES):
    '''
        Error    : the number of all incorrect predictions divided by the total number of the dataset. (FP + FN)/(TP + FP + TN + FN)
        ACCURACY : calculated as the number of all correct predictions divided by the total number of the dataset. (TP + TN)/(TP + FP + TN + FN)
        Sensitivity : the number of correct positive predictions divided by the total number of positives.
                      It is also called recall (REC) or true positive rate (TPR).
                       The best sensitivity is 1.0, whereas the worst is 0.0.
        Specificity: the number of correct negative predictions divided by the total number of negatives. TN/N
        Precision : the number of correct positive predictions divided by the total number of positive predictions
        FScore : F-score is a harmonic mean of precision and recall.


    '''
    print(" GENRE | ERROR | ACCURACY | RECALL | SPECIFICITY | PRECISON | FSCORE ")
    print("_____________________________________________________________")
    for genre, info in genreResultsMap.items():
        if(genre in GENRES):
            tp = info[truePosKey]
            tn = info[trueNegKey]
            fp = info[falsePosKey]
            fn = info[falseNegKey]
            err = calcErr(fp, fn, tp, tn)
            acc = calcAcc(fp, fn, tp, tn)
            recall = calcRecall(tp, fn)
            specificity = calcSpecificity(tn, fn)
            precision = calcPrecision(tp, fp)

            fScore = calcFScore(.5, precision, recall)

            print(genre + "\t" + str(round(err,2)) + "\t" + str(round(acc,2)) + "\t" + str(round(recall,2)) + "\t" + str(round(specificity,2)) +
            "\t" + str(round(precision,2)) + "\t" +str(round(fScore,2)))
    print("\n\n\n")

def initializeConfusionMatrix(genreList):
    confMatrix[numIterationsKey] = 0

    for i in range(len(genreList)):
            toAdd = {}
            genreOfInt = genreList[i]
            toAdd[truePosKey] = 0
            toAdd[falsePosKey] = 0
            toAdd[falseNegKey] = 0
            toAdd[trueNegKey] = 0
            confMatrix[genreOfInt] = toAdd


def getConfMatrix():
    return confMatrix

def analyzeConfusionMatrix(confusionMatrix, genreList):
    global confMatrix

    listSum = compute2dSum(confusionMatrix)

    confMatrix[numIterationsKey] += 1
    for i in range(len(genreList)):
        genreOfInt = genreList[i]
        toAlter = confMatrix[genreOfInt]
        colSum = sum(confusionMatrix[:][i])
        rowSum = sum(confusionMatrix[i])
        truePos = confusionMatrix[i][i]
        toAlter[truePosKey] += truePos
        falsePos = colSum - truePos
        toAlter[falsePosKey] += falsePos
        falseNeg = rowSum - truePos
        toAlter[falseNegKey] += falseNeg
        trueNeg = listSum -falseNeg  - truePos - falsePos
        toAlter[trueNegKey] += trueNeg



    return confMatrix


def computeComplicatedFreqDist(featureMap, GENRES):
    totalGenreLyrics = featureMap["totalGenreLyrics"]
    totalGenreNumVerses = featureMap["totalGenreNumVerses"]

    freqDists = [{} for i in range(len(GENRES))]
    genreTokenLists = [[] for i in range(len(GENRES))]
    genreTypeLists = [[] for i in range(len(GENRES))]

    totalGenreVerses = [0 for i in range(len(GENRES))]
    verseFreqDists = [{} for i in range(len(GENRES))]



    allwords = []
    '''
    Compile all words, numTokens in genreTokenLists, num of distinct tokens in genreTypeLists
    where the i refers to the genre in GENRES[i]
    '''
    for i in range(len(GENRES)):
        genreTokenLists[i] = len(totalGenreLyrics[i])
        genreTypeLists[i] = len(set(totalGenreLyrics[i]))
        allwords.extend(list(set(totalGenreLyrics[i])))

    '''
    Initialize frequency count for the genres
    '''
    for i in range(len(GENRES)):
        genreLyrics = totalGenreLyrics[i]
        for word in genreLyrics:
            currentFreqDist = freqDists[i]
            try:
                currentFreqDist[word] += 1
            except Exception as e:
                currentFreqDist[word] = 1

        genreNumVerses =  totalGenreNumVerses[i] #Get map for numVerses in ith genre for verseFreqDists

        for verseNum in genreNumVerses: #For possible num Verses
            currentGenreFreqDist = verseFreqDists[i]
            tot = genreNumVerses[verseNum]
            currentGenreFreqDist[verseNum] = tot

            totalGenreVerses[i] += tot

    '''
    Process the freqency distributions for each word
    '''
    for i in range(len(freqDists)):
        freqDist = freqDists[i]
        for key in freqDist:
            freqDist[key] = math.log(freqDist[key]) - math.log(genreTokenLists[i])

    for i in range(len(verseFreqDists)):
        freqDist = verseFreqDists[i]
        for key in freqDist:
            freqDist[key] = math.log(freqDist[key]) - math.log(totalGenreVerses[i])

    toRet = {}
    toRet["ngramFreqDists"] = freqDists
    toRet["numVersesFreqDists"] = verseFreqDists

    return toRet


def computeFreqDist(featureMap, GENRES):

    totalGenreLyrics = featureMap["totalGenreLyrics"]
    totalGenreNumVerses = featureMap["totalGenreNumVerses"]
    print(totalGenreNumVerses)

    freqDists = [{} for i in range(len(GENRES))]
    genreTokenLists = [[] for i in range(len(GENRES))]
    genreTypeLists = [[] for i in range(len(GENRES))]



    allwords = []
    '''
    Compile all words, numTokens in genreTokenLists, num of distinct tokens in genreTypeLists
    where the i refers to the genre in GENRES[i]
    '''
    for i in range(len(totalGenreLyrics)):
        genreTokenLists[i] = len(totalGenreLyrics[i])
        genreTypeLists[i] = len(set(totalGenreLyrics[i]))
        allwords.extend(list(set(totalGenreLyrics[i])))

    #for i in range(len(totalGenreNumVerses)):

    '''
    Initialize frequency count for the genres
    '''
    for i in range(len(totalGenreLyrics)):
        genreLyrics = totalGenreLyrics[i]
        for word in genreLyrics:
            currentFreqDist = freqDists[i]
            try:
                currentFreqDist[word] += 1
            except Exception as e:
                currentFreqDist[word] = 1
    '''
    Process the freqency distributions for each word
    '''
    for i in range(len(freqDists)):
        freqDist = freqDists[i]
        for key in freqDist:
            freqDist[key] = math.log(freqDist[key]) - math.log(genreTokenLists[i])

    return freqDists


def calcErr(fp, fn, tp, tn):
    return (fp + fn)/(tp + tn + fn + fp)

def calcAcc(fp, fn, tp, tn):
    return (tp + tn)/(tp + tn + fn + fp)

def calcRecall(tp, fn):
    return (tp)/(tp + fn)

def calcSpecificity(tn, fn):
    return (tn)/(tn + fn)

def calcPrecision(tp, fp):
    return (tp)/(tp + fp)


def calcFScore(beta, prec, recall):
    numer = (1+beta**2.0)*(prec * recall)
    denom = prec + recall
    try: #done to avoid Exception thrown for 0 division
        return numer/denom
    except Exception as e:
        return 0


def compute2dSum(toCount):
    toRet = 0
    for i in range(len(toCount)):
        for j in range(len(toCount[0])):
            toRet += toCount[i][j]
    return toRet
