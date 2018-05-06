import math


truePosKey = "truePos"
trueNegKey = "trueNeg"
falsePosKey = "falsePos"
falseNegKey = "falseNeg"
import ngram_FreqDist

## FUNCTION USING NAIVE BAYES PROBS TO PREDICT SENTIMENT
def naive_bayes(reviewwords, genreList, freqDistLists):
    defaultprob = math.log(0.0000000000001)
    scores = [0 for i in range(len(genreList))]

    toRet = None
    highScore = -float("inf")

    for i in range(len(genreList)):
        freqDist = freqDistLists[i]
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
        reviewWords = ngram_FreqDist.ngrams(song.lyrics, ngramLen)

        positives = song.genres
        result = naive_bayes(reviewWords, genreList, freqDistLists)
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
    displayPerformanceInterpretation(x)

    #for row in range(len(confusionMatrix[0])):
        #print(confusionMatrix[row])

    print("Genres\t", genreList)
    print("Guesses\t", guesses)
    print("Correct Guesses\t", correctGuesses)
    print("Actual Data\t", actual)
    print("Percentage Correct for Genre\t", [round(correctGuesses[i]/actual[i],4) for i in range(len(actual))])
    print("ACCURACY:\t", accuracy)

    return accuracy


def displayPerformanceInterpretation(genreResultsMap):

    print(" GENRE | ACCURACY | RECALL | SPECIFICITY | PRECISON | FSCORE ")
    print("_____________________________________________________________")
    for genre, info in genreResultsMap.items():
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


def analyzeConfusionMatrix(confusionMatrix, genreList):

    toRet = {}

    listSum = compute2dSum(confusionMatrix)
    print(listSum)
    for i in range(len(genreList)):
        toAdd = {}
        genreOfInt = genreList[i]
        colSum = sum(confusionMatrix[:][i])
        rowSum = sum(confusionMatrix[i])
        truePos = confusionMatrix[i][i]
        toAdd[truePosKey] = truePos
        falsePos = colSum - truePos
        toAdd[falsePosKey] = falsePos
        falseNeg = rowSum - truePos
        toAdd[falseNegKey] = falseNeg
        trueNeg = listSum -falseNeg  - truePos - falsePos
        toAdd[trueNegKey] = trueNeg

        toRet[genreOfInt] = toAdd


    return toRet


def compute2dSum(toCount):
    toRet = 0
    for i in range(len(toCount)):
        for j in range(len(toCount[0])):
            toRet += toCount[i][j]
    return toRet

def computeFreqDist(totalGenreLyrics, GENRES):

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
