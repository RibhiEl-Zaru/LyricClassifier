def ngrams(input, n):
    ##Function taking a list and int as inputs to create a list of ngrams
        ##based on the desired n.
    output=[]
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output
