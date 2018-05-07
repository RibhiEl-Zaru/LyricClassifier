import random
def levelData(songs, n, genres):
    newsongs=[]
    random.shuffle(songs)
    for i in genres:
        genre=[]
        count=0
        for s in songs:
            if s.genres[0]==i:
                if count<n:
                    genre.append(s)
                    count+=1
        if len(genre)==n:
            newsongs.extend(genre)
    random.shuffle(newsongs)
    return newsongs

def songCount(songs, genres):
    counts=[]
    for i in genres:
        count=0
        for s in songs:
            if s.genres[0]==i:
                count+=1
        if count>0:
            counts.append([i,count])
    return counts
