#!/usr/bin/env python3
from dataPreprocess import laplacian
from clustering import clustering, label_predictor, rating_predictor
import numpy as np
import scipy as sp
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
#import seaborn

if(__name__ == "__main__"):
    k = 100
    trainfile = input("Input the train file: ")
    test_flag = 0
    if(input("Run test: ") == 'y'):
        testfile = input("Input the test file: ")
        test_flag = 1

    L, matrixID, movieIndex, adjMatrix = laplacian(trainfile)
    
    labels = clustering(L, k, movieIndex)

    # removing movie ids from matrixID according to movieIndex to generate userID = [users]
    # assign each user the label and store the relationship in userLabel = {userID: label}
    # record user rating for each movie in userRating = {userID:{movieID: rating}}
    # record users in each cluster in userCluster = {label: {users}}
    userID = []
    userCluster = {}
    userLabel = {}
    userRating =  {}
    count = 0
    for i in range(0, len(matrixID)):
        if(i not in movieIndex):
            user = matrixID[i]
            userID.append(user)
            userLabel[user] = labels[count]
            count += 1

            userRating[user] = {}
            for j in movieIndex:
                userRating[user][matrixID[j]] = adjMatrix[i][j]
    
    for user, label in userLabel.items():
        if(label not in userCluster):
            userCluster[label] = set()
        userCluster[label].add(user)

    if(test_flag == 1):
        unknown_user_info, movie_user_list = label_predictor(testfile, userLabel)
        predict_results = rating_predictor(unknown_user_info, userCluster, userRating)
        outputFile = open("preds.txt", "w")
        for movie, user in movie_user_list:
            outputFile.write(str(movie) + ',' + str(user) + ',' + str(predict_results[movie][user]) + '\n')
        outputFile.close()




    #if(len(labels) != len(userID)): print("labels and userID not match!")
    #print(userLabel)
    #print(userCluster)
    #print(userRating)
    
    #userCluster = {}
    #for i in range(0, len(userID)):
    #    userCluster[userID[i]] = labels[i]

    

