import webscraper
import os
import sys
from song import Song
import pickle as pickle
import random

def save(listfile, destinationfolder):
#Takes in a file in the following format:
#   song1, artist1
#   song2, artist2, notfound, optionalgenre1, optionalgenre2
#   song3, artist3, notfound
#   etc.
#and loads them into pkl files in the destination folder
    #try:
        f = open(listfile, 'r')
        contents = f.read()
        songs = contents.split('\n')
        for song in songs:
            items = song.split(', ')
            s = None
            if len(items) == 2:
                s = webscraper.getSong(items[0], items[1])
            elif len(items) > 2:
                s = webscraper.getSong(items[0], items[1], items[2], items[3:])
            if s:
    #             name = s.title.replace(' ', '') + '.pkl'
    #             s.saveSong(name, destinationfolder)
    # except Exception as e:
    #     print ('Somthing went wrong...')
    #     print (e)
                namecopy = s.title.replace(' ', '')
                name = ''
                for c in namecopy:
                    if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                        name += c
                i = 1
                while os.path.isfile(os.path.join(destinationfolder, name+'.pkl')):
                    name += str(i)
                    i += 1
                s.saveSong(name+'.pkl', destinationfolder)
    # except Exception as e:
    #     print('Somthing went wrong...')
    #     print(e)

def load(folder, genres=[]):
#Takes in a folder and returns a list of Song objects from the .pkl files it contains
    songs = []
    try:
        for f in os.listdir(folder):
            if f.endswith('.pkl'):
                s = Song.openSong(os.path.join(folder, f))

                s.processLyrics()

                if len(genres)>0:
                    s.filter(genres)
                if len(s.genres)>0:
                    newGenre = []

                    numOfGenres = len(s.genres)
                    choice = random.randint(0,numOfGenres-1)
                    newGenre.append(s.genres[0])
                    s.genres = newGenre
                    songs.append(s)
        return songs
    except Exception as e:
        print('Somthing went wrong...')
        print(e)

def genTrainingAndTestSet(genreToSongs, n):
    '''
     Takes in a list of songs and sorts them by genre (restricted to elements of genres)
      then samples from each bin uniformly n times, returning a new list of songs
     How to Use:
       from loadsongs import *
       songs = clusteredSample(genreToSongs, n)
     where genreToSongs is a map with key-val pair genre to list of songs of that genre
      and n is the desired amount of songs in test set.
    #NOTE: This function is not built to handle all exceptions. It might blow up if you don't treat it nicely

    '''

    d = genreToSongs.copy()

    l = []

    for genre in d:
        random.shuffle(d[genre])
    while len(l)<n:
        g = list(d.keys())
        r1 = int(random.uniform(0, len(g)-1))
        if len(d[g[r1]]) != 0 and len(d[g[r1]]):
            l.append(d[g[r1]].pop(0))
        if len(d[g[r1]])==0:
            g.pop(r1)

    trainSet = []
    for key in d.keys():
        songs = d[key]
        trainSet.extend(songs)

    return ( trainSet, l)

def convertPKLto2(folder, newfolder):
    songs = load(folder)
    for song in songs:
        namecopy = song.title.replace(' ', '')
        name = ''
        for c in namecopy:
            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                name += c
        i = 1
        while os.path.isfile(os.path.join(newfolder, name+'.pkl')):
            name += str(i)
            i += 1
        filename = os.path.join(newfolder, name)+'.pkl'
        f = open(filename, 'wb+')
        pickle.dump(song, f, protocol=2)
    return 'Success'

'''
        Unused code of Shaan Bijwadia and Tiwalayo Eisape

def genreDistribution(songs, genrelist=[]):
#Takes in a list of songs and allowed genres
#prints output based on the number of songs for each genre.
    print('Total number of songs:', len(songs))
    genrecounts = {}
    genrecountcounts = {}
    nogenre = 0
    for song in songs:
        if len(song.genres) in genrecountcounts.keys():
            genrecountcounts[len(song.genres)] += 1
        else:
            genrecountcounts[len(song.genres)] = 1
        for genre in song.genres:
            if len(genrelist)>0 and genre not in genrelist:
                continue
            if genre in genrecounts.keys():
                genrecounts[genre] += 1
            else:
                genrecounts[genre] = 1
    for genre in sorted(genrecounts.items(), key=lambda x: x[1]):
        print(genre[0] + ': ' + str(genre[1]))
    print()
    # print('Number of genres:')
    # for count in genrecountcounts:
    #     print(str(count) + ': ' + str(genrecountcounts[count]))
    # return genrecounts.keys()


if __name__ == '__main__':
    path = None
    sub = 'songs'
    if len(sys.argv) > 0:
        path = sys.argv[0]
    if len(sys.argv) > 1:
        sub = sys.argv[1]
    elif os.path.exists('songlist.txt'):
        path = 'songlist.txt'
    if path:
        save(path, sub)
'''
