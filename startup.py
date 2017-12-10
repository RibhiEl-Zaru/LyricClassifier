import song
from loadsongs import *
from classifier import *
from nHotEncoder import *
from preProcessingUtil import *

#This file provides some basic code to get started with.

folder = 'data/larkin1000_v2' #Replace with a folder of .pkl files containg Song objects


#The line below re-creates a dataset from the RockListMusic.com list and loads them into the directory specified by the 'folder' var.
#NOTE: this code takes a very long time to run. If you would like to try it out, we suggest running it overnight.
#It also creates a .txt file containing info for each song, and a log file to store output.
#loadDataFromAlbums(getLarkin1000(), folder, folder + '.txt', folder + '.log')

#load songs variable with 500 Song objects, using random cluster sampling
songs = load(folder, song.GENRES)
songs = clusteredSample(songs, 500, song.GENRES)

#Print the info for the first 10 songs:
for s in songs[:10]:
    print(s.title, 'by', s.artist+':',s.genres)
print()

#Print the genre frequencies
genreDistribution(songs)

#The most intutive way to import our models for testing is to use model.load()
#first you most reconstruct a model with equivilent structure to the model you wish to test
# you can do this by calling a function from classifiers.py
# next used model.load() on your model to load in pretrained weights
# an example of how to load in a simple Feed Forward model trained on word count is shown below

lyricsList  = [song.simpleLyrics() for song in songs]

data = vectorize(lyricsList, 1).tolist()
inputLayerLength = len(data[0])
nhotLabels = nHotEncoder(songs)


model = modelBuilder(inputLayerLength, 10)
model.fit(np.array(data), np.array(nhotLabels), n_epoch=1, batch_size=50, show_metric=True)
print model.predict(np.array([data[0]]))


# once a model is loaded, to make a prediction used any of our preprocessing utilities
# to structure a string a lyrics into a representation that you model can use
# our simple feed forward with word count model is trained on TF - IDF vector representation of word count
# which can be obtained by running a string of lyrics through our vectorize function


#make a prediction on the first song in our list
model.predict(tfidfs[0])
