def wpmBuckets(songs, genres, n):
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
    min=total[0]
    max=total[len(total)-1]
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
    return wpmGenres
