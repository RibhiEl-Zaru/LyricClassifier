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
import numpy as np
import levelData
import numLinesFreqGenerator
import PairWiseSignTester as signTester
import wpmBuckets
#random.seed(50)

#This file provides some basic code to get started with.

folder = 'data/1001Albums1' #Replace with a folder of .pkl files containg Song objects
GENRES =[
    'folk',
    'rap',
    'rock',
    'r&b',
    'country',
    'blues'
    ]

iterations = 0


#The line below re-creates a dataset from the RockListMusic.com list and loads them into the directory specified by the 'folder' var.
#NOTE: this code takes a very long time to run. If you would like to try it out, we suggest running it overnight.
#It also creates a .txt file containing info for each song, and a log file to store output.
#loaddata.loadDataFromAlbums(loaddata.getLarkin1000(folder), folder, folder + '.txt', folder + '.log')

#load songs variable with 500 Song objects, using random cluster sampling
for i in range(1,3):
    iterations = 0

    ngramLen = i+1
    songs = load(folder, GENRES)
    songs=levelData.levelData(songs, 130, GENRES)
    newsongcount=levelData.songCount(songs, GENRES)
    print(newsongcount)

    GENRES = []
    for i in newsongcount:
        GENRES.append(i[0])

    totalAccuracy = [0 for i in range(len(BM.getConfMatrix()))]

    signTester.initialize()
    print (ngramLen,"-gram analysis")
    BM.initializeConfusionMatrix(GENRES)
    for i in range(50):
        print(i)

        numGenres = len(GENRES)

        counts = [0 for i in range(numGenres)]
        totalGenreLyrics = [[] for i in range(numGenres)]
        totalGenreNumVerses = [{} for i in range(numGenres)]
        totalGenreNumChoruses = [{} for i in range(numGenres)]

        totalGenreWordPerSec = [[] for i in range(numGenres)]


        genreNums = [0 for i in range(numGenres)]
        allGenreLyrics = [[] for i in range(numGenres)]
        numLinesFreqGenerator.initialize(GENRES, 10)
        featureMap = {}
        try:
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
                nGrams = []
                for sentence in sentences:
                    nGram = ngram_FreqDist.ngrams(sentence, ngramLen)
                    nGrams.append(nGram)
                    words = sentence.split()
                    toExtend.append(list(set([w for w in words if w not in stops])))

                #print("    toExtend    ")
                #print(toExtend)

                # To extend is the list of lists with all words tokenize
                allWords = []
                for sentList in toExtend:
                    allWords.extend(sentList)

                s.setnGrams(nGrams)
                # Populate respective genre buckets

                numLinesFreqGenerator.addLineNum(s.numLines) #Add numlines to list containing all totalLine Numbers

                for i in range(len(GENRES)):
                    genre = GENRES[i]

                    if genre in s.genres:
                        try:
                            totalGenreNumVerses[i][s.numVerses] += 1
                        except Exception as e:
                            totalGenreNumVerses[i][s.numVerses] = 1

                        try:
                            totalGenreNumChoruses[i][s.numChoruses] += 1
                        except Exception as e:
                            totalGenreNumChoruses[i][s.numChoruses] = 1

                        if genre in genreToSongs.keys():
                            genreToSongs[genre].append(s)
                        else:
                            genreToSongs[genre] = [s]

                        numLinesFreqGenerator.addLinesForGenre(s.numLines, i) #Add numLines for respective genre

                        counts[i]+= 1 #Update how many of genre X songs there are
                        numGenres += 1 #Keeps track of number of genres for each song

                        for x in toExtend:

                            totalGenreLyrics[i].extend(allWords)

                        genreNums[numGenres] += 1 # Updates how many songs have numGenres amount of genres, as many/all songs have multiple genres according to data.


            featureMap["totalGenreLyrics"] = totalGenreLyrics
            featureMap["totalGenreNumVerses"] = totalGenreNumVerses
            featureMap["totalGenreNumChoruses"] = totalGenreNumChoruses




            freqDists = BM.computeFreqDist(featureMap, GENRES)
            numLinesFreqMap = numLinesFreqGenerator.generateFrequencyMap()
            wpmMap = wpmBuckets.wpmBuckets(songs, GENRES, 10)
            freqDists["wpmFreqDists"]=wpmMap

            freqDists["numLinesFreqDists"] = numLinesFreqMap
            accuracy = BM.naiveBayesSentimentAnalysis(testSet, GENRES, freqDists, ngramLen)

            x = None
            y = None

            for i in range(len(accuracy)):

                instanceAcc = accuracy[i]
                totalAccuracy[i] += instanceAcc
                if(i == 0):
                    x = instanceAcc
                if (i == 1):
                    y = instanceAcc

            signTester.addPair(x,y)
            iterations += 1
        except Exception as e:

            raise


        '''

                                DETAILS OF GENERATED LISTS

            percentages : The chance that a random song is of each genre, as ordered by index shown in GENRES list.

            binomialProbab : output of function in preProcessingUtil.py.

                             Returns the true chance of correctly guessing the genre of a song,
                             factoring in that each song has a different amount of "correct" genres



        '''

        #percentages = [round(i/sum(counts) * 100 , 4) for i in counts]

        #for i in range(len(percentages)):
        #    print("Data is : " + str(percentages[i])  + "% " + GENRES[i], "   with a total of  "  , counts[i])


    confMatrix = BM.getConfMatrix()
    BM.displayPerformanceInterpretation(confMatrix, GENRES)
    for i in range(len(totalAccuracy)):
        print("The results of bayes number ", i )
        acc = totalAccuracy[i]
        avgAccuracy  = acc /iterations
        print(avgAccuracy)

    #TODO Handle the PairWiseSignTester

    signTester.evaluateTests()


binomialProbab = generateRandomProbability(genreNums, GENRES)
print("True random success rate is: ", round(binomialProbab,4))




def calcTotal(genreToSongs):
    tot = 0
    for key in genreToSongs.keys():
        tot += len(genreToSongs[key])
    return tot


allGenreLyrics = [[] for i in range(len(GENRES))]
songs = load(folder, GENRES)
trainingSet, testSet = train.train_test(songs, GENRES)
allTokSentences = []
for s in trainingSet:
    tokSentences = []
    sentences = s.lyrics.rstrip().splitlines()
    songGenre = ''.join(s.genres)
    index = GENRES.index(songGenre)
    for sentence in sentences:
        tokSentence = word_tokenize(sentence)
        if len(tokSentence) == 0:
            continue
        tokSentences.append(tokSentence)
        for word in tokSentence:
            allGenreLyrics[index].append(word)
    s.setTokenizedSentences(tokSentences)
    allTokSentences.extend(tokSentences)

model = gensim.models.Word2Vec(allTokSentences, size=100, window=5, min_count=1, workers=4)
##model.save("word2vecModel.model")
allGenreVectors = [[] for i in range(len(GENRES))]
for i in range(len(GENRES)):
    vector = np.zeros((100,), dtype=float)
    for j in range(len(allGenreLyrics[i])):
        wordArray = model.wv[allGenreLyrics[i][j]]
        vector = np.add(vector,wordArray)
    divisor = np.full((100,), len(allGenreLyrics[i]))
    vector = np.divide(vector,divisor)
    allGenreVectors[i] = vector

correct = 0.0
total = 0.0
for s in testSet:
    sentences = s.lyrics.rstrip().splitlines()
    songGenre = ''.join(s.genres)
    index = GENRES.index(songGenre)
    tokSentences = []
    for sentence in sentences:
        tokSentence = word_tokenize(sentence)
        tokSentences.append(tokSentence)
    s.setTokenizedSentences(tokSentences)

    songVector = s.vectorizeSong(model)
    correctGenre = s.genres[0]
    answer = s.returnVectorGenre(songVector, allGenreVectors)

    if str(correctGenre) == answer:
        correct += 1
    total += 1
print ("Percent correct is: " , correct/total)


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
