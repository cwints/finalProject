library(readxl)
library(DescTools)

#import each table from the dataset
Original_Data_Order_Items <- read_excel("493 Final Project/Original_Data.xlsx", 
                                     sheet = "Order_Items")
View(Original_Data_Order_Items)

Original_Data_Geography <- read_excel("493 Final Project/Original_Data.xlsx", 
                                        sheet = "Geography")
View(Original_Data_Geography)

Original_Data_Orders <- read_excel("493 Final Project/Original_Data.xlsx", 
                                      sheet = "Orders")
View(Original_Data_Orders)

Original_Data_Customer <- read_excel("493 Final Project/Original_Data.xlsx", 
                                   sheet = "Customer")
View(Original_Data_Customer)

Original_Data_Product <- read_excel("493 Final Project/Original_Data.xlsx", 
                                     sheet = "Product")
View(Original_Data_Product)

Isolated_Order_Items <- Original_Data_Order_Items[,c(3,4,7)] #isolate Order Number, N_items and Order_ID
View(Isolated_Order_Items)

Isolated_Geography <- Original_Data_Geography[,c(3,4)] #isolate country and country code
View(Isolated_Geography)

Isolated_Orders <- Original_Data_Orders[,c(2,3,4,7)] #isolate Order number, Customer_ID, Order_Date and N_items
View(Isolated_Orders)

Isolated_Customer <- Original_Data_Customer[,c(2,3,4,5)] #isolate Customer_ID, Country, Gender and Birthday
View(Isolated_Customer)

Isolated_Product <- Original_Data_Product[,c(2,3,4)] #isolate Product_ID, List Price and Description
View(Isolated_Product)

mergedCustandGeo<- merge(x=Isolated_Geography,y=Isolated_Customer,by="Country_Code") #merge modified Customer and Geography tables
View(mergedCustandGeo)

mergedOrders<- merge(x=Isolated_Order_Items,y=Isolated_Orders,by="Order_Number",all=TRUE) #merge modified Order Items and Order tables
View(mergedOrders)

ProductandOrders <- merge(x=mergedOrders,y=Isolated_Product,by="Product_ID") #merge previous order merge with modified Product tables
View(ProductandOrders)

EverythingMerged <- merge(x=ProductandOrders,y=mergedCustandGeo,by="Customer_ID") #merge the previous product and order merge with the merged customer and geography table
View(EverythingMerged)

EverythingMerged$N_Items.x <- NULL #delete the repeated N_items column 

write.csv(EverythingMerged, 'Cleaned_Data.csv') #save the result as a csv 
