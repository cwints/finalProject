def dict_search(value,key,dict_list):
    """This function searches for a specific value in a list of dictionaries and
    outputs a list of the dictionairies who carry this value. The a paramaters
    are (1) The desired value to search for, (2) the dictionary key associated
    with this value, (3) the list of dictionaries to search in.
    """
    search_results = []
    for dicts in dict_list:
        if dicts[key] == value:
            search_results.append(dicts)
    return search_results

def purchased_together(value,dict_list,key1 = "Product_ID", key2 = "Order_Number"):
    """This function returns the items purchased in combination with a specified
    item. The parameters are: (1) The ID of the product we want to find items
    purchased with, (2) the list of dictionaries containing order data to search
    through, (3) the key "Product ID" set by default, (4) the key "Order_Number"
    also set by default.
    """
    search_results = []
    relevant_product = []
    search_results_final = []
    for dicts in dict_list:
       if dicts[key1] == value:
           relevant_product.append(dicts)
    for products in relevant_product:
        for dicts in dict_list:
            if dicts[key2] == products[key2]:
                search_results.append(dicts)
    for dicts in search_results:
        del dicts["Customer_ID"], dicts["Order_Number"], dicts["Order_Date"]
        del dicts["N_Items"], dicts["Country_Code"], dicts["Country"]
        del dicts["Gender"], dicts["Birthday"]
        if dicts[key1] != value :
            search_results_final.append(dicts)
    return search_results_final

def wtp (value, dict_list, key1="Customer_ID" , key2="List_Price", key3 = "N_Items"):
    """This function returns a specified customer's average purchase price per
    item, along with their number of number of purchases and the standard deviation
    of this average purchase price (expressed as a %). Parameters are: (1)the
    Customer ID of the customer, (2)the transaction data as a list of dictionaries,
    and (3) key1, (4) key2, and (5) key3 are optional raguments defaulting to 
    the appropriate dictionary keys to complete the search and calculations.
    """
    import numpy as np
    cust_dicts = []
    price_list = []
    order_size = []
    for dicts in dict_list:
        if dicts[key1] == value:
            cust_dicts.append(dicts)
    counter = 0
    total_val = 0
    for dicts in cust_dicts:
        price_list.append(float(dicts[key2]))
        order_size.append(float(dicts[key3]))
        total_val += float(dicts[key2])
        counter += 1
    wtp_val = round((total_val/counter),2)
    sd_dol = round(np.std(price_list),2)
    total = 0
    for item in order_size:
        total += item
    avg_size = round(total/len(order_size),2)
    cust_wtp = {key1:value, "WTP": wtp_val, "Products_Purchased": counter, "SD ($)":sd_dol, "Avg. Order Size (# of items)" : avg_size}
    return cust_wtp
        
            

if __name__ == "__main__":
    from AI_dict_converter import csv_to_dict
    file = "Cleaned_Data_Search_3.csv"
    dict_list = csv_to_dict(file)
    value = '700002'
    key = "Customer_ID"
    search_results = dict_search(value, key, dict_list)
    print("\n")
    for items in search_results:
        print(items, end="\n\n")
    print("---------------------------------")
    dict_list = csv_to_dict(file)
    purchased_results = purchased_together("102010903", dict_list)
    for items in purchased_results:
        print(items, end= "\n\n")
    #print(len(purchased_results))
    print("---------------------------------")
    dict_list = csv_to_dict(file)
    wtp = wtp(value,dict_list)
    print(wtp)
    
        

