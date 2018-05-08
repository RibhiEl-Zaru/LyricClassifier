import scipy.stats as st

pairs = []
u = 0
n = 0
alpha = .05

def initialize():
    global pairs
    global n
    global u
    pairs = []
    n = 0
    u = 0


def evaluateTests():
    global u
    u = 0

    calculateU()
    zScore = calculateZScore()
    pVal = getPScore(zScore)

    print("N is equal to ", n)
    print("P-value of test is ", pVal)

def addPair(x, y):
    global pairs
    global n
    pairs.append((x,y))
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
    denom = (n/4.)**(1./2.)
    print(denom)
    zscore = numer/denom
    return zscore

def getAlphaZ():
    return st.norm.ppf(1- alpha)

def getPScore(zScore):
    p_value = st.norm.sf(abs(zScore)) #one-sided
    return p_value
