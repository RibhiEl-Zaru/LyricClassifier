import song
import loaddata
#import wordCloudGenerator as wcg
from loadsongs import *
from classifier import *
from nHotEncoder import *
from preProcessingUtil import *
import spotifyclient
from train_test_sets import *

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

counts = [0 for i in range(len(GENRES))]
totalGenreLyrics = ["" for i in range(len(GENRES))]
genreNums = [0 for i in range(len(GENRES))]

#The line below re-creates a dataset from the RockListMusic.com list and loads them into the directory specified by the 'folder' var.
#NOTE: this code takes a very long time to run. If you would like to try it out, we suggest running it overnight.
#It also creates a .txt file containing info for each song, and a log file to store output.
#loaddata.loadDataFromAlbums(loaddata.getLarkin1000(folder), folder, folder + '.txt', folder + '.log')

#load songs variable with 500 Song objects, using random cluster sampling




songs = load(folder, GENRES)
train, test = train_test(songs)


total = 0
for s in songs: #Populate the various buckets
    total += 1
    numGenres = 0
    for i in range(len(GENRES)):
        genre = GENRES[i]
        if genre in s.genres:
            counts[i]+= 1 #Update how many of genre X songs there are
            numGenres += 1 #Keeps track of number of genres for each song
            totalGenreLyrics[i]= totalGenreLyrics[i] + s.lyrics

    genreNums[numGenres] += 1 # Updates how many songs have numGenres amount of genres, as many/all songs have multiple genres according to data.
    #print(s.title, 'by', s.artist+':',s.genres, " with popularity ", s.popularity, s.duration_ms)


#wcg.saveWordClouds(GENRES, totalGenreLyrics)

'''

                        DETAILS OF GENERATED LISTS

    percentages : The chance that a random song is of each genre, as ordered by index shown in GENRES list.

    binomialProbab : output of function in preProcessingUtil.py.

                     Returns the true chance of correctly guessing the genre of a song,
                     factoring in that each song has a different amount of "correct" genres

'''

percentages = [round(i/sum(counts) * 100 , 4) for i in counts]

for i in range(len(percentages)):
    print("Data is : " + str(percentages[i])  + "% " + GENRES[i] )


binomialProbab = generateRandomProbability(genreNums, GENRES)
print("True random success rate is: ", round(binomialProbab,4))


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
