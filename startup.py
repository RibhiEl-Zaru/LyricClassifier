import song
from nltk.corpus import stopwords
import loaddata
#import wordCloudGenerator as wcg
from loadsongs import *
from classifier import *
from nHotEncoder import *
from preProcessingUtil import *
import math
import bayesianModel as BM
import spotifyclient
import train_test_sets as train
import gensim
from ngram_FreqDist import *
import ngram_FreqDist
#random.seed(50)

#This file provides some basic code to get started with.

folder = 'data/1001Albums1' #Replace with a folder of .pkl files containg Song objects
GENRES = [
'folk',
'rap',
'rock',
'r&b',
'country',
'blues'
]

iterations = 1

counts = [0 for i in range(len(GENRES))]
totalGenreLyrics = [[] for i in range(len(GENRES))]
genreNums = [0 for i in range(len(GENRES))]
allGenreLyrics = [[] for i in range(len(GENRES))]
totalAccuracy = 0


#The line below re-creates a dataset from the RockListMusic.com list and loads them into the directory specified by the 'folder' var.
#NOTE: this code takes a very long time to run. If you would like to try it out, we suggest running it overnight.
#It also creates a .txt file containing info for each song, and a log file to store output.
#loaddata.loadDataFromAlbums(loaddata.getLarkin1000(folder), folder, folder + '.txt', folder + '.log')

#load songs variable with 500 Song objects, using random cluster sampling

ngramLen = 3
songs = load(folder, GENRES)
print(len(songs))

for i in range(iterations):
    total = 0

    stops = stopwords.words('english')
    genreToSongs = {}

    trainingSet, testSet = train.train_test(songs, GENRES)
    allTokSentences = []
    for s in trainingSet: #Populate the various buckets
        total += 1
        numGenres = 0
        sentences = s.lyrics.rstrip().splitlines()
        songGenre = ''.join(s.genres)
        index = GENRES.index(songGenre)
        #print("    SENTENCES    ")
        #print(sentences)
        #Build the sentences that we'd need to add
        toExtend = []
        tokSentences = []
        for sentence in sentences:
            tokSentence = ngram_FreqDist.ngrams(sentence, ngramLen)
            for word in tokSentence:
                allGenreLyrics[index].append(word)
            tokSentences.append(tokSentence)
            words = sentence.split()
            toExtend.append(list(set([w for w in words if w not in stops])))

        #print("    toExtend    ")
        #print(toExtend)

        # To extend is the list of lists with all words tokenized
        allTokSentences.extend(tokSentences)
        allWords = []
        for sentList in toExtend:
            allWords.extend(sentList)

        s.setTokenizedSentences(tokSentences)

        # Populate respective genre buckets
        for i in range(len(GENRES)):
            genre = GENRES[i]

            if genre in s.genres:
                if genre in genreToSongs.keys():
                    genreToSongs[genre].append(s)
                else:
                    genreToSongs[genre] = [s]
                counts[i]+= 1 #Update how many of genre X songs there are
                numGenres += 1 #Keeps track of number of genres for each song

                for x in toExtend:

                    totalGenreLyrics[i].extend(allWords)

                genreNums[numGenres] += 1 # Updates how many songs have numGenres amount of genres, as many/all songs have multiple genres according to data.

    freqDists = BM.computeFreqDist(totalGenreLyrics, GENRES)

    accuracy = BM.naiveBayesSentimentAnalysis(testSet, GENRES, freqDists, ngramLen)
    totalAccuracy += accuracy
    '''

                            DETAILS OF GENERATED LISTS

        percentages : The chance that a random song is of each genre, as ordered by index shown in GENRES list.

        binomialProbab : output of function in preProcessingUtil.py.

                         Returns the true chance of correctly guessing the genre of a song,
                         factoring in that each song has a different amount of "correct" genres



    '''

    percentages = [round(i/sum(counts) * 100 , 4) for i in counts]

    for i in range(len(percentages)):
        print("Data is : " + str(percentages[i])  + "% " + GENRES[i], "   with a total of  "  , counts[i])


    binomialProbab = generateRandomProbability(genreNums, GENRES)
    print("True random success rate is: ", round(binomialProbab,4))


avgAccuracy  = totalAccuracy /iterations
print(avgAccuracy)

def calcTotal(genreToSongs):
    tot = 0
    for key in genreToSongs.keys():
        tot += len(genreToSongs[key])
    return tot

'''
'''
##model = gensim.models.Word2Vec(allTokSentences, size=100, window=5, min_count=1, workers=4)
##print(model.wv['love'])
##print(model.wv['and'])








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
