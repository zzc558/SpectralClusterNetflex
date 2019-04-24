#!/usr/bin/env python3
import numpy as np

def laplacian(filename):
#if(__name__ == "__main__"): 
    #filename = "example01.csv"
    trainFile = open(filename, "r")
    trainFile.readline()
    matrixID = []
    movieIndex = []
    A = []
    movie_record = {}
    user_record = {}

    trainFile.readline()
    for line in trainFile:
        c = line.split(',')
        movie = int(c[0])
        user = int(c[1])
        rate = int(c[2])
        #time = int(c[3].split('-')[0])
        if(movie not in movie_record):
            movie_record[movie] = len(matrixID)
            movieIndex.append(len(matrixID))
            matrixID.append(movie)
            for ls in A:
                ls.append(0)
            tmp = []
            for i in range(0, len(matrixID)):
                tmp.append(0)
            A.append(tmp)
        if(user not in user_record):
            user_record[user] = len(matrixID)
            matrixID.append(user)
            for ls in A:
                ls.append(0)
            tmp = []
            for i in range(0, len(matrixID)):
                tmp.append(0)
            A.append(tmp)
        i = movie_record[movie]
        j = user_record[user]
        A[i][j] = rate
        A[j][i] = rate

    trainFile.close()

    D = np.zeros((len(matrixID), len(matrixID)))
    W = np.array(A)
    S = np.sum(W, axis=0)
    D.flat[::len(S) + 1] = S ** (-0.5)
    I = np.identity(len(matrixID))
    #L = I - D.dot(W).dot(D)
    return I - D.dot(W).dot(D), matrixID, movieIndex, A