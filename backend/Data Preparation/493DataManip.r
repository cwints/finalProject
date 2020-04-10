setwd("~/Queen's Commerce/4th Year/Semester 2/COMM 493 AI/Team Project")

library(readxl)
library(DescTools)
Original_Data_Unedited <- read_excel("Queen's Commerce/4th Year/Semester 2/COMM 493 AI/Team Project/Original-Data-Unedited.xlsx", 
                                     sheet = "Order_Items")
View(Original_Data_Unedited)

###########################################

masterData <- Original_Data_Unedited
View(masterData)

masterDataT <- masterData[,c(3,9)] #isolate product ID and order ID
View(masterDataT)

uniqueProducts <-  unique(masterDataT[,2]) #482 unique products
View(uniqueProducts)

uniqueOrders <-  unique(masterDataT[,1])
View(uniqueOrders) #114 unique orders # Products * orders = 54948

crossData <-  merge(x = uniqueOrders, y = uniqueProducts, by = NULL)
View(crossData)

colnames(crossData)[2] <- "productTag" 
joinedMaster <-  merge(x = crossData, y = masterDataT, by = "Order Number", all = TRUE)
View(joinedMaster)

result <-  ifelse(joinedMaster$productTag == joinedMaster$Product_ID,1,0) 
#if a product is purchased in an order, flag itzas 1, else 0
View(result)

joinedFlagged <- cbind(joinedMaster,result)
View(joinedFlagged)

preFinal <- joinedFlagged[,-3]
View(preFinal)
finalMaster <- (unique(preFinal))
View(finalMaster)

write.csv(finalMaster, 'finalMaster.csv')



