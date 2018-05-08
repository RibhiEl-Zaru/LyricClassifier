min=None
step=None
max=None
bucknums=None
def wpmBuckets(songs, genres, n):
    global bucknums
    bucknums=n
    wpmGenres=[[i] for i in genres]
    buckets=[[]for x in range(n)]
    total=[]
    for s in songs:
        words=[]
        sentences = s.lyrics.rstrip().splitlines()
        for sentence in sentences:
            word = sentence.split()
            words.extend(word)
        wpm=len(words)/float(s.duration_ms)
        total.append(wpm)
    length = round(len(total)/float(n))
    total.sort()
    global min
    min=total[0]
    global max
    max=total[len(total)-1]
    global step
    step=(max-min)/float(n)

    for s in songs:
        words=[]
        sentences = s.lyrics.rstrip().splitlines()
        for sentence in sentences:
            word = sentence.split()
            words.extend(word)
        wpm=len(words)/float(s.duration_ms)
        index=int((wpm-min)//step)
        if wpm==max:
            buckets[n-1].append(s)
            continue
        buckets[index].append(s)
    lenbucks=[len(buckets[i])for i in range(len(buckets))]
    for dex in buckets:
        for s in dex:
            for gen in wpmGenres:
                if s.genres[0]==gen[0]:
                    gen.append(buckets.index(dex))


    #Now to generate frequency map:
    freqMaps = [{} for i in range(len(genres))]
    for i in range(len(genres)):
        genreList = wpmGenres[i]
        currFreqMap = freqMaps[i]
        t=0
        for score in genreList[1:]:
            try:
                currFreqMap[score] += 1
            except:
                currFreqMap[score] =1

    return freqMaps

def bucketize(wpm):
    index=int((wpm-min)//step)
    if wpm==max:
        index=bucknums-1
    return index
