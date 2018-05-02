import math



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

def naiveBayesSentimentAnalysis(testData, genreList, freqDistLists):
    numCorrect = 0
    guesses = [0 for i in range(len(genreList))]
    correctGuesses = [0 for i in range(len(genreList))]
    actual =  [0 for i in range(len(genreList))]
    for song in testData:
        reviewWords = song.lyrics
        genres = song.genres

        result = naive_bayes(reviewWords, genreList, freqDistLists)
        guesses[genreList.index(result)] += 1
        for genre in genres:
            if genre == result:
                numCorrect += 1
                correctGuesses[genreList.index(result)] += 1
            actual[genreList.index(genre)] += 1
    accuracy = numCorrect/len(testData)
    print("Genres\t", genreList)
    print("Guesses\t", guesses)
    print("Correct Guesses\t", correctGuesses)
    print("Actual Data\t", actual)
    print("Percentage Correct for Genre\t", [round(correctGuesses[i]/actual[i],4) for i in range(len(actual))])
    print("ACCURACY:\t", accuracy)
    return accuracy


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
