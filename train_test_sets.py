import random
def train_test(songs):
    #Takes in a list of Song objects and randomly separates it into:
        #80% training set and 20% testing set.
    #Thus maintaining the original proportionality of genres in the two sets.
    cut = round(len(songs)*.8)
    random.shuffle(songs)
    train = songs[:cut]
    test = songs[cut:]
    return train, test
