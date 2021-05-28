# Predict_the_Price_of_Used_Cars

#### I have secured the rank 41 out of 2608 participants.
#### DataSet Link : https://machinehack.com/hackathons/predicting_the_costs_of_used_cars_hackathon_by_imarticus_learning/data
#### LeaderBoard Link : https://machinehack.com/hackathons/predicting_the_costs_of_used_cars_hackathon_by_imarticus_learning/leaderboard

#### Challenges : 
1) Data cleaning is an important part of this challenge.
2) There are a lot of null values in the dataset . Also there are almost 86% null values in the column name New_Price which is an important column to predict the old sale price of car
3) Some values in New_Price column is given as integer.There are some values where lakhs are writtern with values and there are some values where crores are written with values
4) 'CC' is given with column engine.
5) 'KM/PL' or 'KM/KG' is given with column mileage

#### Findings :
1) There is a correlation between Year column and target column
2) There is huge impact of column New_Price in predicting the old car sale price
3) Column Owner_Type also effect the old sale price of car
4) Due to more categorical column and more no. of categories in categorical columns I used Categorical boost which provide accuracy on test set 93.80% and Light GBM which provides accuracy on test set 93.29 %

#### Below is the application link
#### https://old-car-price-prediction1.herokuapp.com

![Screenshot](https://user-images.githubusercontent.com/19778041/119949235-4c013500-bfb7-11eb-85c5-799262747612.png)
