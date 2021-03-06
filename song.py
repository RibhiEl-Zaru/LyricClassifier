import spotifyclient
import pickle as pickle
from nltk.tokenize import word_tokenize
import os
import nltk
import numpy as np
import scipy

GENRES = [
'folk',
'rap',
'rock',
'r&b',
'country',
'blues'
]

class Song(object):
    """
    Object containing the lyrics to a single song
    Attributes:
            lyrics: string containing song lyrics
            genres: list containing genres
            title: string containing song title (optional)
            artist: string containing primary artist (optional)
            numVerses: integer containing number of verses in song
            numChoruses: integer containing number of choruses in song
            numLines: integer containing number of lines in song
    """
    def __init__(self, lyrics,genres, title='', artist='', popularity = 0, duration_ms = 0, notfound='ignore'):
    #Constructor takes in local variables and option if genre is not found thru Spotify client
        self.lyrics = lyrics
        self.title = title.replace('\n', '')
        self.artist = artist.replace('\n', '')
        self.genres = genres if notfound=='add' else []

        self.genres = genres if (notfound=='replace' or notfound=='add') else []
        self.popularity = popularity
        self.duration_ms = duration_ms
        self.numVerses = 0
        self.numLines = 0
        self.numChoruses = 0
        self.nGrams = None
        self.songVector = None
        self.tokenizedSentences = None

        if len(genres)==0 or notfound=='add':
            artistgenres = spotifyclient.getArtistProperties(self.artist, GENRES)
            if artistgenres:
                for g in artistgenres:
                    self.genres.append(g)
            elif notfound == 'prompt':
                genres = raw_input('Genres not found, please input: ').split(',')
                if len(genres) > 0:
                    self.genres = genres

    def filter(self, allowed):
    #Takes in a list of allowed genres and updates self.genres
    #returns a list of removed genres
        removed = []
        new = []

        for g in self.genres:
            for a in allowed:
                if a not in new and a in g:
                    new.append(a)
                else:
                    removed.append(g)
        self.genres = new
        return removed

        '''
        for g in self.genres:
            for a in allowed:
                if g == a and a not in new:
                    new.append(a)
                else:
                    removed.append(g)
        self.genres = new
        return removed
        '''

    def tokens(self):
        return word_tokenize(self.simpleLyrics())
#throws out all lyrics after mismatched bracket

    #Must handle this to update self, and
    def  processLyrics(self):
    #Removes "[Chorus]", "[Verse X]", etc., punctuation, and newlines


        self.numChoruses = 0
        self.numVerses = 0
        self.numLines = 0
        lyrics = self.lyrics.lower()

        i = 0
        allowedChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \''
        simpleLyrics = ''
        #print("-------- ORIGINAL LYRICS --------")
        #print(self.lyrics)
        while i < len(lyrics): #I think this is bad practice. w/e
            c = lyrics[i]
            if c in allowedChars:
                simpleLyrics += c
            if c=='[':
                if lyrics[i+1].lower() == 'v':
                    self.numVerses = self.numVerses + 1
                elif lyrics[i+1].lower() == 'c':
                    self.numChoruses = self.numChoruses + 1

                while i<len(lyrics) and lyrics[i]!=']':
                    i +=1
            elif c == '\n':
                self.numLines +=1
                simpleLyrics += '\n'
            elif c == '\t':
                simpleLyrics += '\n'

            i+=1

        self.lyrics =  simpleLyrics

        #print("-------- SIMPLE LYRICS --------")
        #print(self.lyrics)

    def tokenFrequencies(self):
    #Takes in a string of song lyrics and returns a dictionary containing
    #each unique word in the lyrics and its frequency
        lyrics = self.simpleLyrics()
        words = word_tokenize(lyrics)
        freq = {}
        for word in words:
            if word in freq:
                freq[word] += 1
            elif not word=='':
                freq[word] = 1
        return freq


    def setnGrams(self, sents):
        self.nGrams = sents

    def setTokenizedSentences(self, sents):
        self.tokenizedSentences = sents

    def saveLyrics(self, filename):
    #Saves title artist, lyrics to file at filename (creates a file if none exists)
    #NOTE: To save the entire Song object, use saveSong()
        f = open(filename, 'w+')
        f.write(self.title+'\n')
        f.write(self.artist+'\n')
        f.write(self.lyrics+'\n')
        f.close()

    def saveSong(self, filename, subdirectory=''):
    #Saves Song object to file at filename, which can include a subdirectory
        if len(subdirectory) == 0:
            f = open(filename, 'wb+')
        else:
            try:
                os.mkdir(subdirectory)
            except Exception:
                pass
            f = open(os.path.join(subdirectory, filename), 'wb+')
        pickle.dump(self, f, protocol=2)

    def vectorizeSong(self, model):
        word_vectors = model.wv
        words = []
        notFound = 0
        vector = np.zeros((100,), dtype=float)
        for sent in self.tokenizedSentences:
            for word in sent:
                words.append(word)
        if len(words) == 0:
            return np.zeros((100,), dtype=float)
        for word in words:
            if word in word_vectors.vocab:
                wordVector = model.wv[str(word)]
                vector = np.add(vector,wordVector)
            else:
                notFound += 1

        divisor = np.full((100,), (len(words) - notFound), dtype=float)
        vector = np.divide(vector,divisor)
        self.songVector = vector
        return vector

    def returnVectorGenre(self, wordVector, allGenreVectors):
        min = 1
        index = 0
        for i in range(len(allGenreVectors)):
            distance = scipy.spatial.distance.cosine(wordVector,allGenreVectors[i])
            if (distance < min):
                min = distance
                index = i
        return GENRES[index]



    @staticmethod
    def openLyrics(filename):
    #Returns new Song object with title, artist, and lyric drawn from file at filename
    #NOTE: To open an entire Lyric object, use openSong()
        f = open(filename, 'r')
        contents = f.read()
        title = contents[:contents.index('\n')]
        contents = contents[contents.index('\n')+1:]
        artist = contents[:contents.index('\n')]
        lyrics = contents[contents.index('\n')+1:]
        return Song(lyrics, title, artist)

    @staticmethod
    def openSong(filename):
    #Returns a new Song object with all data drawn from filename
        f = open(filename, 'rb')
        return pickle.load(f)
