#!/usr/bin/env python3
from dataPreprocess import laplacian
import numpy as np
import scipy as sp
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def clustering(matrix, k, movieIndex):
    eValue, eVector = sp.sparse.linalg.eigs(matrix, k, which='SM')

    # get rid of the movie nodes
    count = 0
    for i in movieIndex:
        eVector = np.delete(eVector, i - count, axis=0)
        count += 1

    eVector_real = eVector.real
    eVec_row_norm = np.linalg.norm(eVector_real, ord=2, axis=1)
    eVector_norm = (eVector_real.T / eVec_row_norm).T

    kmeans = KMeans(n_clusters=k, random_state=1231).fit(eVector_norm)
    return kmeans.labels_
    #labels = kmeans.labels_

    #fh = open("label.txt", "w+")
    #for value in labels:
    #    fh.write(str(value))
    #fh.close()

def label_predictor(fname, userLabel):
    testFile = open(fname, 'r')
    #testFile.readline()

    userInfo = {}
    movie_user_list = []
    for line in testFile:
        c = line.split(',')
        movie = int(c[0])
        user = int(c[1])
        movie_user_list.append((movie, user))
        #time = int(c[3].split('-')[0])
        if(user not in userLabel):
            print("Unknown user in test set:", user)
            continue
        
        if(user not in userInfo):
            userInfo[user] = []
            userInfo[user].append(userLabel[user])

        userInfo[user].append(movie)
    
    testFile.close()
    return userInfo, movie_user_list

# get average rating for the movie from users with the same label
def get_rating(label, movie, clusterDict, ratingDict):
    users = clusterDict[label]
    rating = set()
    for user in users:
        rating.add(ratingDict[user][movie])
    return int(sum(rating) / len(rating) + 0.5)

# get predict rating value for every movie in movieRating = {movie:{user: rating}}
def rating_predictor(userDict, clusterDict, ratingDict):
    movieRating = {}
    for user, info in userDict.items():
        label = info.pop(0)
        for movie in info:
            if(movie not in movieRating):
                movieRating[movie] = {}
            movieRating[movie][user] = get_rating(label, movie, clusterDict, ratingDict)
    return movieRating
            


