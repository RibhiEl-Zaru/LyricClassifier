import scipy.stats as st

pairs = []
u = 0
n = 0
alpha = .05

def initialize():
    global pairs
    pairs = []
    n = 0


def addPair(x, y):
    global pairs
    global n
    pairs.append((x,y))
    print(pairs)
    n += 1


def calculateU():
    global u
    for pair in pairs:
        x = pair[0]
        y = pair[1]

        if(x > y):
            u += 1
    return u


def calculateZScore():
    numer = u - n/2
    denom = (u/4)**(1./2.)
    zscore = numer/denom
    return zscore

def getAlphaZ():
    return st.norm.ppf(1- alpha)

def getPScore(zScore):
    p_value = st.norm.sf(abs(zScore)) #one-sided
    return p_value
