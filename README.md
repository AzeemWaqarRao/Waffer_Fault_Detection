# Waffer_Fault_Detection

## Project OverView
The Waffer Fault Detection project in Python involves using machine learning algorithms to detect and classify defects on silicon waffers in semiconductor manufacturing.

## Dataset:
For each Waffer we get values from 500+ sensors and based on that we tell whether the waffer is functioning(+1) or faulty(-1)<br />
[Click Here to get Data](https://drive.google.com/drive/folders/1R-za-a7adbyAnBMDYNWWWQbHuJzTVc0A?usp=share_link)


## Architecture:
<img width="838" alt="architecture" src="https://user-images.githubusercontent.com/61060465/228646336-23514c1c-865d-4ba7-b80c-bea7bdb0ec46.png">

## Data Validation:
In this step, we perform different steps of validation like,<br />
Is the filename valid?<br />
Are all columns present?<br />
Name of each column<br />
Data type of each columns<br /> 

## Data Insertion in Database
In this step we perform the following things,<br />
Database Creation and connection<br />
Table creation in the database<br />
Insertion of files in the table<br />

## Model Training
### Data Export from Db:
The data in a stored database is exported as a CSV file to be used for model training.<br />
### Data Preprocessing:
In this step we check for null values in each column. If null values are present we use KNN Imputer to fill in those values with the mean of k neighbours of it.<br />
Also we will remove the columns which have a standard deviation of 0, it means all the values in that column are same and hence that column won't add any meaning to the model training.<br />
### Clustering:
The idea behind clustering is to find enteries(rows) that are relatively similar to each other, create cluster and train separte model for each cluster. This Technique lets us get better accuracy by grouping similar data together.<br />
We use Kmeans to cluster of preprocessed data and save the model for later use.
### Model Selection:
After clusters are created, we find the best model for each cluster. Two algorithms are used RandomForest and XGBoost. We perform Grid Search CV to get both models for best paramenters and then compare their accuracy to get the better model.<br />


## Model Prediction
Here also all the above steps like Data Validation, Data Insertion in Database, Data Preprocessing and Clustering is performed. Based on the cluster group, the model is loaded and prediction is made.

## Project Screen
![output-screen](https://user-images.githubusercontent.com/61060465/228653602-f94d8877-572d-4ebe-a80b-09d8d5ce3628.png)
