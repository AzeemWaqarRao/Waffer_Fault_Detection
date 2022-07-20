import pandas as pd
from sklearn.impute import KNNImputer

class Preprocessor:

    def preprocess(self):
        data = pd.read_csv("Training_Data.csv")
        data = self.removeColumns(data)


        X,y = self.splitData(data)

        isNull = self.isNull(data)

        if(isNull):
            X = self.imputeNullValues(X)
            X.to_csv("X.csv")

        X = self.dropColwithZeroStd(X)
        X.to_csv("X.csv")




    def removeColumns(self,data):

        data = data.drop(['Wafer'],axis=1)
        return data

    def splitData(self,data):


        X = data.iloc[:, 1:-1]
        y = data.iloc[:, -1]
        X.to_csv('X.csv')
        y.to_csv('y.csv')
        return X,y

    def isNull(self,data):

        isNull = False
        null_count = data.isna().sum()
        for i in null_count:
            if i>0:
                isNull = True
                break

        if(isNull):
            null_df = (pd.DataFrame(data.isna().sum()))
            null_df.to_csv("Model/null_data_count.csv")

        return isNull

    def imputeNullValues(self,data):
        data = pd.DataFrame(data)

        impute = KNNImputer(n_neighbors=5, weights="uniform")
        temp = impute.fit_transform(data)
        data = pd.DataFrame(temp,columns=data.columns)
        return data


    def dropColwithZeroStd(self,data):
        data = pd.DataFrame(data)

        dic = data.describe()

        for i in data.columns:
            if dic[i]['std'] == 0:
                data = data.drop([i],axis=1)

        return data