"""This module contains a function that converts CSV files into a list of
dictionaries. 
"""


def csv_to_dict(csv_file):
    """This function converts a csv file (parameter is the file's  name) into
    a list of dictionaries, which it returns.
    """
    import csv
    data_list = []
    dict_list = []
    with open(csv_file,"r") as file:
        reader = csv.reader(file)
        for row in reader:
            data_list.append(row)
        for i in range(1,len(data_list)):
            temp_dict = {}
            for j in range(0, len(data_list[1])):
                temp_dict[data_list[0][j]] = data_list[i][j]
                j + 1
            dict_list.append(temp_dict)
            i + 1
        return dict_list
                
            
            
        
    

if __name__ == "__main__": #testing
    file = "Cleaned_Data_Search_3.csv"
    dict_list = csv_to_dict(file)
    for dict_item in dict_list:    
        print(dict_item)
    
        
