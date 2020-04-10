# Import Dependencies
from flask import Flask, render_template, url_for, request
import os
import pandas as pd
import numpy as np
from backend.AI_dict_converter import csv_to_dict
import backend.AI_knn_consolidated as ai
import backend.AI_search_algos as search
import backend.utility_functions as utility

app = Flask(__name__)

# load homepage
@app.route('/')

def index():
    return render_template('index.html')

# load page where a user can search by customer id or name and email
@app.route('/customer')
 
def customerHome():
    return render_template('customer-home.html')

# load product page where a user can search by product id or filter by product attributes
@app.route('/product')

def productHome():
    return render_template('product-home.html')


# Load the customer search results page with customers matching the search criteria 
@app.route('/customer_search')

def customerSearch():
    df = pd.read_csv("backend/Customer List.csv")
    df = utility.findSearchResultsCustomer(df, request.args.get("firstName"), request.args.get("lastName"), request.args.get("email"))
    df = df[["Customer_ID","First_Name","Last_Name","Email"]]
    outputList = df.values.tolist()
    return render_template('customer-search.html', list = outputList)

# Load the product search results page with products matching the search criteria
@app.route('/product_search')

def productSearch():
    df = pd.read_csv("backend/Product List.csv") # Load dataframe of product information
    df = utility.findSearchResultsProduct(df, request.args.get("category"), request.args.get("colour"), request.args.get("design"), request.args.get("pattern"))
    outputList = df.values.tolist()
    return render_template('product-search.html', list = outputList)

# Load customer results page if a customer id is in the database otherwise it will redirect the user to
# the search results page
@app.route('/customer_result')

def idSearchCustomer():
    dictList = csv_to_dict("backend/Cleaned_Data_Search_3.csv")
    df = pd.read_csv("backend/Customer List.csv")
    productDf = pd.read_csv("backend/Product List.csv")
    customerID = int(request.args.get("customerID"))
    row = df["Customer_ID"] == customerID
    newDF = df[row]
    if newDF.shape[0] == 1:
        wtp = search.wtp(str(customerID),dictList)
        priceRangeLow, priceRangeHigh = wtp['WTP'] - wtp['SD ($)'], wtp['WTP'] + wtp['SD ($)'] 
        wtp['Price Range'] = '$' + f'{priceRangeLow:.2f}' + ' - $' + f'{priceRangeHigh:.2f}'
        mostRecentPurchases = ai.mostRecentPurchases(str(customerID),dictList, 5)
        productIDList = [i['Product_ID'] for i in mostRecentPurchases]
        recommendations = ai.recosForRecentPurchases(productIDList[0:2])
        recommendationsList = utility.getProductInfo(productDf, recommendations)
        firstName, lastName, email, country, gender, birthday = newDF['First_Name'], newDF['Last_Name'], newDF['Email'], newDF['Country'], newDF['Gender'], newDF['Birthday']
        return render_template('customer-result.html', firstName = firstName.item(), lastName = lastName.item(), customerID = customerID, email = email.item(), country = country.item(), gender = gender.item(), birthday = birthday.item(), wtp = wtp, mostRecentPurchases = mostRecentPurchases, recommendations = recommendationsList)
    else:
        outputList = newDF.values.tolist()
        return render_template('customer-search.html', list = outputList)

# Load the customer results page when a users choses the customer from the search results page
@app.route('/customer_result/<id>')

def customerResult(id):
    df = pd.read_csv("backend/Customer List.csv")
    productDf = pd.read_csv("backend/Product List.csv")
    dictList = csv_to_dict("backend/Cleaned_Data_Search_3.csv")
    row = df['Customer_ID'] == int(id)
    newDF = df[row]
    wtp = search.wtp(id,dictList)
    priceRangeLow, priceRangeHigh = wtp['WTP'] - wtp['SD ($)'], wtp['WTP'] + wtp['SD ($)'] 
    wtp['Price Range'] = '$' + f'{priceRangeLow:.2f}' + ' - $' + f'{priceRangeHigh:.2f}'
    mostRecentPurchases = ai.mostRecentPurchases(id,dictList, 5)
    productIDList = [i['Product_ID'] for i in mostRecentPurchases]
    recommendations = ai.recosForRecentPurchases(productIDList[0:3])
    recommendationsList = utility.getProductInfo(productDf, recommendations)
    firstName, lastName, email, country, gender, birthday = newDF['First_Name'], newDF['Last_Name'], newDF['Email'], newDF['Country'], newDF['Gender'], newDF['Birthday']
    return render_template('customer-result.html', firstName = firstName.item(), lastName = lastName.item(), customerID = int(id), email = email.item(), country = country.item(), gender = gender.item(), birthday = birthday.item(), wtp = wtp, mostRecentPurchases = mostRecentPurchases, recommendations = recommendationsList)


# Load the product results page a valid product ID is entered
# Otherwise resdirect the user to the search page
@app.route('/product_result')

def idSearchProduct():
    dictList = csv_to_dict("backend/Cleaned_Data_Search_3.csv")
    clusters = pd.read_csv("backend/Clusters.csv")
    df = pd.read_csv("backend/Product List.csv")
    productID = int(request.args.get("productID"))
    row = df["Product_ID"] == productID
    newDF = df[row]
    if newDF.shape[0] == 1:
        name, price, colour, category, design, pattern = newDF['Description'], newDF['List_Price'], newDF['Colour'], newDF['Category'], newDF['Design'], newDF['Pattern']
        purchased_together = search.purchased_together(str(productID),dictList)
        recosFromPreviousPurchasesList = ai.kNNbAlgo(productID)
        recosFromPreviousPurchases = utility.getProductInfo(df, recosFromPreviousPurchasesList)
        kMeansRecosList = utility.kMeansRecommendations(clusters, productID,recosFromPreviousPurchasesList,6)
        kMeansRecos = utility.getProductInfo(df, kMeansRecosList)
        return render_template('product-result.html', name = name.item(), productID = productID, price = price.item(), colour = colour.item(), category = category.item(), design = design.item(), pattern = pattern.item(), recosFromPreviousPurchases = recosFromPreviousPurchases,  kMeansRecos=kMeansRecos, purchased_together = purchased_together )
    else:
        outputList = newDF.values.tolist()
        return render_template('product-search.html', list = outputList)

# Load the product results page when a users choses the product from the search results page
@app.route('/product_result/<id>')

def productResult(id):
    dictList = csv_to_dict("backend/Cleaned_Data_Search_3.csv")
    df = pd.read_csv("backend/Product List.csv")
    clusters = pd.read_csv("backend/Clusters.csv")
    row = df['Product_ID'] == int(id)
    newDF = df[row]
    name, price, colour, category, design, pattern = newDF['Description'], newDF['List_Price'], newDF['Colour'], newDF['Category'], newDF['Design'], newDF['Pattern']
    purchased_together = search.purchased_together(str(id),dictList)
    recosFromPreviousPurchasesList = ai.kNNbAlgo(id)
    recosFromPreviousPurchases = utility.getProductInfo(df, recosFromPreviousPurchasesList)
    kMeansRecosList = utility.kMeansRecommendations(clusters, int(id),recosFromPreviousPurchasesList,6)
    kMeansRecos = utility.getProductInfo(df, kMeansRecosList)
    return render_template('product-result.html', name = name.item(), productID = int(id), price = price.item(), colour = colour.item(), category = category.item(), design = design.item(), pattern = pattern.item(), recosFromPreviousPurchases = recosFromPreviousPurchases,  kMeansRecos=kMeansRecos, purchased_together = purchased_together)


port = os.getenv('PORT', '5010')
if __name__ == "__main__":
    app.run(debug = True, port=int(port))