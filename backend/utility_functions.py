
# Search by the criteria selected for the product search and return a datframe with products
# that match the filters
def findSearchResultsProduct(df, category, colour, design, pattern):
    searchList = [category, colour, design, pattern]
    searchIndex = ['Category', 'Colour', 'Design', 'Pattern']
    for i in range(len(searchList)):
        if searchList[i] != "any":
            df = df[df[searchIndex[i]]== searchList[i]]
    return df


# Search by the criteria selected for the customer search and return a datframe with customers
# that match the filters
def findSearchResultsCustomer(df, firstName, lastName, email):
    searchList = [firstName, lastName, email]
    searchIndex = ['First_Name', 'Last_Name', 'Email']
    for i in range(len(searchList)):
        if searchList[i] != "":
            df = df[df[searchIndex[i]]== searchList[i]]
    return df


#Returns a df with product information given a list a of product IDs
def getProductInfo(df, productIDs):
    outputList = []
    for i in productIDs:
        productInfo = df[df["Product_ID"] == int(i)]
        if productInfo.shape[0] > 0:
            outputList.append(productInfo.values[0])
    return outputList


#Search the pretrain kMeans model output to determine what cluster a product belongs to
#Finds other products that also belong in the same cluster
#Remove duplicate recommendations from knn recommendations
#Returns the number of recomendations as specific in the parameters 
def kMeansRecommendations(df, productID, otherRecos,numRecos):
    cluster = int(df[df['Product_ID'] == productID]['Cluster'].values[0])
    recoDf = df[df['Cluster']== cluster]
    recoDf = recoDf[recoDf['Product_ID']!= productID]
    for i in otherRecos:
        recoDf = recoDf[recoDf['Product_ID'] != int(i)]
    return recoDf.iloc[0:numRecos,0]