import pandas as pd

class Preprocessor:

    def preprocess(self):
        data = pd.read_csv("Training_Data.csv")
        data = self.removeColumns(data)


        X,y = self.splitData(data)

        self.isNull(data)




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