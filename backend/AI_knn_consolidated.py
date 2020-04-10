# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:57:16 2020

@author: metro
"""

import io
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from surprise import KNNBasic
from surprise import Reader
from surprise import Dataset
from surprise import KNNBaseline

def kNNbAlgo(product_ID, nRecos=3): 
    """
    Adapted from class tutorial, uses the KNN Baseline algorithm of the Surprise library for recommendation. 
    Data must follow an explicit format, per below. As such, data is recasted using R into "finalMaster.csv".
    
    Function returns a list of n recommended products in product ID format, 
    where n is 3 by default but can be specified if desired. 
    
    Function takes a product ID as the only required parameter. 
    """
    
    reader = Reader(line_format='user item rating', sep=',')
    data = Dataset.load_from_file('backend/finalMaster.csv', reader=reader)
    trainset = data.build_full_trainset()

    sim_options = {'name': 'pearson_baseline', 'user_based': False}
    algo = KNNBaseline(sim_options=sim_options)
    algo.fit(trainset)

    product_inner_id = algo.trainset.to_inner_iid(str(product_ID))
    product_neighbors = algo.get_neighbors(product_inner_id, k=nRecos)
    product_neighbors = (algo.trainset.to_raw_iid(inner_id)
                           for inner_id in product_neighbors)

    recoList = list(product_neighbors)

    return recoList

def mostRecentPurchases (value, dict_list, n, key1="Customer_ID"):
    """    
    This function returns a specific customer's n most recent purchases, 
    from most recent to least recent.
    
    Returned is the full data of their purchase, expressed as a dictionary. Parameters are:
    (1) the customer ID (2) the transaction data as a list of dictionaries, (3)
    the number of purchases desired and (4) a default key to lookup values by the customer ID

    """
    import datetime    
    cust_dicts = []
    refined_dict = {}
    for dicts in dict_list:
        if dicts[key1] == value:
            cust_dicts.append(dicts)
            
    if int(n) > len(cust_dicts):
        n = len(cust_dicts)
            
    for item in cust_dicts:
        itemDateElements = item['Order_Date'].split('/')
        itemDate = datetime.date(int(itemDateElements[2]),int(itemDateElements[1]),int(itemDateElements[0]))
        item['Order_Date_New'] = itemDate
        
    sortedcustDicts = sorted(cust_dicts, key=(lambda k: k['Order_Date_New']), reverse=True)
    
    return sortedcustDicts[:n] #returns a list of dictionaries of n most recent purchases.

def recosForRecentPurchases (productIDList,m=2):
    
    """
    This intermediate function calls the kNN function for each product ID in a list of products 
    (assumed to be the n most recently purchased products by a given customer), and outputs the top m
    recommendations per product, for a total of n*m recommendations (by default, 3*2 = 6). The function includes
    a check for duplicate recommendations, in which case it reruns the KNN with an expanded scope to get the next 
    best recommendation. 
    
    This function outputs a list of recommended items, in product ID format. 
    
    This funtion takes a list of product IDs as input, to be fed into the KNN. The m parameter specifies the 
    number of recommendations to get back from the KNN algorithm (e.g. top m recommended items) and is set to
    2 by default. This assumes 6 recommendations per customer (3 most recent items, 2 recos per item). 
    
    """
    
    recoList = []
    for product_ID in productIDList:
        for reco in kNNbAlgo(product_ID, m):
            i = m
            while reco in recoList: 
                # this while loop ensures there are no duplicates in the recommended products 
                # by expanding the range of the recommendation algo until there is no duplicate
                output = (kNNbAlgo(product_ID,i+1)) 
                reco = output[i]
                i +=1
            recoList.append(reco)
    return recoList

if __name__ == "__main__":
    from AI_dict_converter import csv_to_dict
    import datetime
    
    file = "Cleaned_Data_Search_3.csv"
    dict_list = csv_to_dict(file)
    
    outputList = mostRecentPurchases('100001',dict_list, 3) 
    #for a given customer ID, returns three most recent purchases
    
    for item in outputList:
        print(item,end="\n\n")
    #output for testing 
          
    productIDListForReco = []
    
    for item in outputList:
        productIDListForReco.append(item['Product_ID'])
    #create a list of just the product IDs from the most recent purchases
    #this is needed because the most recent purchases function outputs a list of dictionaries while the recos 
    #function requires a list of product IDs.
    
    kNNRecos = recosForRecentPurchases(productIDListForReco)
    print(kNNRecos)
    # calls the KNN for each of these products and outputs recos as a list of product IDs
    