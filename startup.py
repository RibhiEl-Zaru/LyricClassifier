import song
from nltk.corpus import stopwords
import loaddata
import wordCloudGenerator as wcg
from loadsongs import *
from classifier import *
from nHotEncoder import *
from preProcessingUtil import *
import math
import spotifyclient

#This file provides some basic code to get started with.

folder = 'data/1001Albums0' #Replace with a folder of .pkl files containg Song objects
GENRES = [
'pop',
'rap',
'rock',
'r&b',
'country',
'blues'
]

## FUNCTION USING NAIVE BAYES PROBS TO PREDICT SENTIMENT
def naive_bayes(reviewwords, genreList, freqDistLists):
    defaultprob = math.log(0.0000000000001)
    scores = [0 for i in range(len(genreList))]

    toRet = None
    highScore = -float("inf")
    for i in range(len(genreList)):
        freqDist = freqDistLists[i]
        score = freqDist.get(reviewwords[0], defaultprob)
        for i in range(1, len(reviewwords)):
            score += freqDist.get(reviewwords[i], defaultprob)

        if score > highScore:
            highScore = score
            toRet = GENRES[i]

    return toRet

counts = [0 for i in range(len(GENRES))]
totalGenreLyrics = [[] for i in range(len(GENRES))]
genreTokenLists = [[] for i in range(len(GENRES))]
genreTypeLists = [[] for i in range(len(GENRES))]
freqDists = [{} for i in range(len(GENRES))]
genreNums = [0 for i in range(len(GENRES))]

#The line below re-creates a dataset from the RockListMusic.com list and loads them into the directory specified by the 'folder' var.
#NOTE: this code takes a very long time to run. If you would like to try it out, we suggest running it overnight.
#It also creates a .txt file containing info for each song, and a log file to store output.
#loaddata.loadDataFromAlbums(loaddata.getLarkin1000(folder), folder, folder + '.txt', folder + '.log')

#load songs variable with 500 Song objects, using random cluster sampling




songs = load(folder, GENRES)


total = 0

stops = stopwords.words('english')

for s in songs: #Populate the various buckets
    total += 1
    numGenres = 0
    sentences = s.lyrics.rstrip().splitlines()
    #print("    SENTENCES    ")
    #print(sentences)
    #Build the sentences that we'd need to add
    toExtend = []
    for words in sentences:
        words = words.split()
        toExtend.append(list(set([w for w in words if w not in stops])))

    #print("    toExtend    ")
    #print(toExtend)

    # To extend is the list of lists with all words tokenized
    allWords = []
    for sentList in toExtend:
        allWords.extend(sentList)

    s.setTokenizedSentences(allWords)

    # Populate respective genre buckets
    for i in range(len(GENRES)):
        genre = GENRES[i]

        if genre in s.genres:
            counts[i]+= 1 #Update how many of genre X songs there are
            numGenres += 1 #Keeps track of number of genres for each song

            for x in toExtend:

                totalGenreLyrics[i].extend(allWords)

            genreNums[numGenres] += 1 # Updates how many songs have numGenres amount of genres, as many/all songs have multiple genres according to data.

'''

    This is how we generate wordclouds.

wcg.saveWordClouds(GENRES, totalGenreLyrics)

'''

'''
Compile all words, numTokens in genreTokenLists, num of distinct tokens in genreTypeLists
where the i refers to the genre in GENRES[i]
'''
allwords = []
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



'''

                        DETAILS OF GENERATED LISTS

    percentages : The chance that a random song is of each genre, as ordered by index shown in GENRES list.

    binomialProbab : output of function in preProcessingUtil.py.

                     Returns the true chance of correctly guessing the genre of a song,
                     factoring in that each song has a different amount of "correct" genres



percentages = [round(i/sum(counts) * 100 , 4) for i in counts]

for i in range(len(percentages)):
    print("Data is : " + str(percentages[i])  + "% " + GENRES[i] )


binomialProbab = generateRandomProbability(genreNums, GENRES)
print("True random success rate is: ", round(binomialProbab,4))


'''






'''
#songs = clusteredSample(songs, 500, song.GENRES)




#lyricsList  = [song.simpleLyrics() for song in songs]
#print(lyricsList[1])


#Print the genre frequencies
genreDistribution(songs)

# Instead of including models weights which sized in the hundreds of megabytes, here
# we provide a quick tutorial to quickly train and deploy a text classifier

# First, transform your song list into a list of simple lyrics stripped of punctuation
# and auxilary characters


#Vectorize using functions from preProcessUtil.py
data = vectorize(lyricsList, 1).tolist()
inputLayerLength = len(data[0])

#Computes nhot labels based on the genre distribution of each given song
nhotLabels = nHotEncoder(songs)

# modelBuilder returns a model with parameters describe in our write up
# here is an example of our most standard model
model = modelBuilder(inputLayerLength, 10)
model.fit(np.array(data), np.array(nhotLabels), n_epoch=20, batch_size=50, show_metric=True)

#returns a probabilty distribution over each of our possible genres
print model.predict(np.array([data[0]]))

'''
