import math
import ngram_FreqDist
import numLinesFreqGenerator

truePosKey = "truePos"
trueNegKey = "trueNeg"
falsePosKey = "falsePos"
falseNegKey = "falseNeg"
numIterationsKey = "numIters"

confMatrixes = [{}, {}] # First map is basic bayes, second map is bayes with features
## FUNCTION USING NAIVE BAYES PROBS TO PREDICT SENTIMENT

def naiveBayesWithFeatures(featureMap, genreList, freqMaps):

    defaultprob = math.log(0.0000000000001)
    scores = [0 for i in range(len(genreList))]

    baseReturn = None
    advancedReturn = None

    baseHighScore = -float("inf")
    advancedHighScore = -float("inf")


    reviewwords = featureMap["reviewwords"]
    numVerses = featureMap["numVerses"]
    numChoruses = featureMap["numChoruses"]
    numLines = featureMap["numLines"]

    ngramFreqDists = freqMaps["ngramFreqDists"]
    numVersesFreqDists = freqMaps["numVersesFreqDists"]
    numChorusesFreqDists = freqMaps["numChorusesFreqDists"]
    numLinesFreqDists = freqMaps["numLinesFreqDists"]


    reviewWordLen = len(reviewwords)

    for i in range(len(genreList)):
        ngramFreqDist = ngramFreqDists[i]
        numVersesFreqDist = numVersesFreqDists[i]
        numChorusesFreqDist = numChorusesFreqDists[i]
        numLinesFreqDist = numLinesFreqDists[i]

        baseScore = ngramFreqDist.get(reviewwords[0], defaultprob)
        for j in range(1, reviewWordLen):
            baseScore += ngramFreqDist.get(reviewwords[j], defaultprob)

        if(baseScore > baseHighScore):
            baseHighScore = baseScore
            baseReturn = genreList[i]

        advancedScore = baseScore + numVersesFreqDist.get(numVerses, defaultprob)*reviewWordLen
        advancedScore += numChorusesFreqDist.get(numChoruses, defaultprob) * reviewWordLen
        advancedScore += numLinesFreqDist.get(numLinesFreqGenerator.bucketizeScore(numLines), defaultprob) * reviewWordLen

        if(advancedScore > advancedHighScore):
            advancedHighScore = advancedScore
            advancedReturn = genreList[i]

    return [baseReturn, advancedReturn]


def naiveBayesSentimentAnalysis(testData, genreList, freqDistLists, ngramLen):

    confusionMatrixes = [ [[0 for i in range(len(genreList))]for i in range(len(genreList))] for i in range(len(confMatrixes))]

    numCorrect = [0 for i in range(len(confMatrixes))]
    guesses = [[0 for i in range(len(genreList))]for i in range(len(confMatrixes))]
    correctGuesses = [[0 for i in range(len(genreList))]for i in range(len(confMatrixes))]
    actual =  [0 for i in range(len(genreList))]

    for song in testData:
        if(len(song.lyrics)<ngramLen):
            continue;

        reviewWords = ngram_FreqDist.ngrams(song.lyrics, ngramLen)

        positives = song.genres

        featureMap = {}
        featureMap["reviewwords"] = reviewWords
        featureMap["numVerses"] = song.numVerses
        featureMap["numChoruses"] = song.numChoruses
        featureMap["numLines"] = song.numLines


        results = naiveBayesWithFeatures(featureMap, genreList, freqDistLists)

        for i in range(len(results)):
            result = results[i]
            guesses[i][genreList.index(result)] += 1

            c = genreList.index(result)
            for genre in positives:
                r = genreList.index(genre)
                confusionMatrixes[i][r][c]+= 1

            for genre in positives:
                if genre == result:
                    numCorrect[i] += 1
                    correctGuesses[i][genreList.index(result)] += 1
                actual[genreList.index(genre)] += 1

    x = analyzeConfusionMatrixes(confusionMatrixes, genreList)
    #displayPerformanceInterpretation(x)

    #for row in range(len(confusionMatrix[0])):
        #print(confusionMatrix[row])


    accuracy = [correct/len(testData) for correct in numCorrect]
    '''
    print("Genres\t", genreList)
    print("Guesses\t", guesses)
    print("Correct Guesses\t", correctGuesses)
    print("Actual Data\t", actual)
    print("Percentage Correct for Genre\t", [round(correctGuesses[i]/actual[i],4) for i in range(len(actual))])
    print("ACCURACY:\t", accuracy)
    '''
    return accuracy


def displayPerformanceInterpretation(confMatrixes, GENRES):
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
    index = 0
    for genreResultsMap in confMatrixes:
        print("ConfidenceMatrix number " , index)
        index += 1
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
    for confMatrix in confMatrixes:

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
    return confMatrixes

def analyzeConfusionMatrixes(confusionMatrixes, genreList):
    global confMatrixes

    for i in range(len( confusionMatrixes)):
        confMatrix = confMatrixes[i]
        confusionMatrix = confusionMatrixes[i]
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



    return confMatrixes


def computeFreqDist(featureMap, GENRES):
    numGenres = len(GENRES)
    totalGenreLyrics = featureMap["totalGenreLyrics"]
    totalGenreNumVerses = featureMap["totalGenreNumVerses"]
    totalGenreNumChoruses = featureMap["totalGenreNumChoruses"]

    freqDists = [{} for i in range(numGenres)]
    genreTokenLists = [[] for i in range(numGenres)]
    genreTypeLists = [[] for i in range(numGenres)]

    totalGenreVerses = [0 for i in range(numGenres)]
    totalGenreChoruses = [0 for i in range(numGenres)]

    verseFreqDists = [{} for i in range(numGenres)]
    chorusFreqDists = [{} for i in range(numGenres)]


    allwords = []
    '''
    Compile all words, numTokens in genreTokenLists, num of distinct tokens in genreTypeLists
    where the i refers to the genre in GENRES[i]
    '''
    for i in range(numGenres):
        genreTokenLists[i] = len(totalGenreLyrics[i])
        genreTypeLists[i] = len(set(totalGenreLyrics[i]))
        allwords.extend(list(set(totalGenreLyrics[i])))

    '''
    Initialize frequency count for the genres
    '''
    for i in range(numGenres):
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

        genreNumChoruses =  totalGenreNumChoruses[i] #Get map for numChoruses in ith genre for chorusFreqDists

        for chorusNum in genreNumChoruses:
            currentGenreFreqDist = chorusFreqDists[i]
            tot = genreNumChoruses[chorusNum]
            currentGenreFreqDist[chorusNum] = tot

            totalGenreChoruses[i] += tot


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

    for i in range(len(chorusFreqDists)):
        freqDist = chorusFreqDists[i]
        for key in freqDist:
            freqDist[key] = math.log(freqDist[key]) - math.log(totalGenreChoruses[i])

    toRet = {}
    toRet["ngramFreqDists"] = freqDists
    toRet["numVersesFreqDists"] = verseFreqDists
    toRet["numChorusesFreqDists"] = chorusFreqDists

    return toRet



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
