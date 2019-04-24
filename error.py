#!/usr/bin/env python3

#def MSE(predRating, actRating):

if(__name__ == "__main__"):
    fname = input("Input the test file name: ")
    predFile = open("preds.txt", 'r')
    predDict = {}
    for line in predFile:
        c = line.split(",")
        movie = int(c[0])
        user = int(c[1])
        rating_pred = int(c[2])
        if(movie not in predDict):
            predDict[movie] = {}
        predDict[movie][user] = rating_pred
    predFile.close()

    testFile = open(fname, "r")
    actDict = {}
    for line in testFile:
        c = line.split(",")
        movie = int(c[0])
        user = int(c[1])
        rating_act = int(c[2])
        if(movie not in actDict):
            actDict[movie] = {}
        actDict[movie][user] = rating_act
    testFile.close()

    SE = 0
    for movie in predDict:
        for user in predDict[movie]:
            rating_pred = predDict[movie][user]
            rating_act = actDict[movie][user]
            SE += (rating_pred - rating_act) ** 2

    print(SE / len(predDict))

