import random


trainTestSplit= [.80, .20]

def train_test(songs, genres):
    #Takes in a list of Song objects and randomly separates it into:
        #80% training set and 20% testing set.
    #Thus maintaining the original proportionality of genres in the two sets.
    train=[]
    test=[]
    trainTestAmount=[round(len(songs)*i) for i in trainTestSplit]
    random.shuffle(songs)
    for i in genres:
        amount=0
        for s in songs:
            if s.genres[0]==i:
                amount+=1
        proportion= amount/float(len(songs))
        x=0
        total = round(trainTestAmount[0]*proportion)
        print("Total "+i+": "+str(total))
        for s in songs:
            if s.genres[0]==i:
                if x < total:
                    train.append(s)
                    x+=1
                else:
                    test.append(s)
        #if random.randint(1,100)>trainTestSplit[0]:
            #test.append(i)
        #else:
            #train.append(i)
    #cut = round(len(songs)*trainTestSplit[0])
    #random.shuffle(songs)
    #train = songs[:cut]
    #test = songs[cut:]
    return train, test
