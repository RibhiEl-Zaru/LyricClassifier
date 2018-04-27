import song
import loaddata
from loadsongs import *
from classifier import *
from nHotEncoder import *
from preProcessingUtil import *
import spotifyclient

#This file provides some basic code to get started with.

folder = 'data/1001Albums' #Replace with a folder of .pkl files containg Song objects
GENRES = [
'pop',
'rap',
'rock',
'r&b',
'country',
'jazz',
'electronic',
]
counts = [0 for i in range(len(GENRES))]

genreNums = [0 for i in range(len(GENRES))]

#The line below re-creates a dataset from the RockListMusic.com list and loads them into the directory specified by the 'folder' var.
#NOTE: this code takes a very long time to run. If you would like to try it out, we suggest running it overnight.
#It also creates a .txt file containing info for each song, and a log file to store output.
#loaddata.loadDataFromAlbums(loaddata.getLarkin1000(folder), folder, folder + '.txt', folder + '.log')

#load songs variable with 500 Song objects, using random cluster sampling


songs = load(folder, GENRES)
total = 0
for s in songs:
    total += 1
    numGenres = 0
    for i in range(len(GENRES)):
        genre = GENRES[i]
        if genre in s.genres:
            counts[i]+= 1
            numGenres += 1

    genreNums[numGenres] += 1


    #print(s.title, 'by', s.artist+':',s.genres, " with popularity ", s.popularity, s.duration_ms)

print(counts)
print(total)
print(sum(counts))
percentages = [str(round(i/total * 100 , 4)) + "%" for i in counts]
print(percentages)

print(genreNums)

binomialProbab = generateRandomProbability(genreNums, GENRES)

print("True random success rate is: ", round(binomialProbab,4))


songs = clusteredSample(songs, 500, song.GENRES)
#print((songs[:20]))
'''
for s in songs[:10]:
    print(s.title, 'by', s.artist+':',s.genres)
    print(s.lyrics)
print()

#Print the info for the first 10 songs:


#Print the genre frequencies
genreDistribution(songs)

# Instead of including models weights which sized in the hundreds of megabytes, here
# we provide a quick tutorial to quickly train and deploy a text classifier

# First, transform your song list into a list of simple lyrics stripped of punctuation
# and auxilary characters
lyricsList  = [song.simpleLyrics() for song in songs]

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
