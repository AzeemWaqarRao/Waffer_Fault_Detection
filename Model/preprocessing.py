import inspect
import os
from Logger.logger import Logger
import pandas as pd
from sklearn.impute import KNNImputer


class Preprocessor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = Logger()
        self.file = open(os.path.join("Training_Logs", "trainingPreprocessingLogs.txt"), mode='a+')

    def preprocess_train(self):
        try:
            self.logger.log(self.file, "Training Data Preprocessing Started")
            data = pd.read_csv(self.file_path)
            data = self.removeColumns(data)

            X, y = self.split_data(data)

            isNull = self.isNull(data)

            if (isNull):
                X = self.imputeNullValues(X)
                X.to_csv("X.csv")

            X = self.dropColwithZeroStd(X)
            X.to_csv("X.csv")
            self.logger.log(self.file, "Training Data Preprocessing Completed")

        except Exception as e:
            self.logger.log(self.file, "Exception %s occurred while Preprocessing Training Data" % e)
            raise e
        self.file.close()


    def preprocess_predict(self):


        self.file.close()
        self.file = open(os.path.join("Prediction_Logs", "predictionPreprocessingLogs.txt"), mode='a+')
        try:
            self.logger.log(self.file, "Prediction Data Preprocessing Started")
            data = pd.read_csv(self.file_path)
            wafer = data['Wafer']
            data = self.removeColumns(data)
            data = data.iloc[:, 1:]

            isNull = self.isNull(data)

            if isNull:
                data = self.imputeNullValues(data)

            data = self.dropColwithZeroStd(data)
            data['Wafer'] = wafer
            data.to_csv(self.file_path)
            self.logger.log(self.file, "Prediction Data Preprocessing Completed")

        except Exception as e:
            self.logger.log(self.file, "Exception %s occurred while Preprocessing Prediction Data" % e)
            raise e

        self.file.close()


    def removeColumns(self, data):

        try:
            data = data.drop(['Wafer'], axis=1)
            self.logger.log(self.file, "Preprocessing : Columns Removed Successfully")
            return data

        except Exception as e:
            self.logger.log(self.file, "Preprocessing : Columns Removed Failure %s" % e)
            raise e

    def split_data(self, data):

        try:
            X = data.iloc[:, 1:-1]
            y = data.iloc[:, -1]
            X.to_csv('X.csv')
            y.to_csv('y.csv')
            self.logger.log(self.file, "Preprocessing : Label separation Successfully")

            return X, y

        except Exception as e:
            self.logger.log(self.file, "Preprocessing : Label Separation Failure %s" % e)

            raise e

    def isNull(self, data):

        try:
            isNull = False
            null_count = data.isna().sum()
            for i in null_count:
                if i > 0:
                    isNull = True
                    break

            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            parent = calframe[1][3]

            if (isNull):
                null_df = (pd.DataFrame(data.isna().sum()))

                if parent == "preprocess_train":
                    null_df.to_csv("Model/null_data_count_training.csv")
                    self.logger.log(self.file,
                                    "Preprocessing : Null values count saved in null_data_count_training.csv")

                else:
                    null_df.to_csv("Model/null_data_count_prediction.csv")
                    self.logger.log(self.file, "Preprocessing : Null values count saved in "
                                               "null_data_count_prediction.csv")

            return isNull

        except Exception as e:
            self.logger.log(self.file, "Preprocessing : Error in isNull method : %s" % e)
            raise e

    def imputeNullValues(self, data):

        try:
            data = pd.DataFrame(data)

            impute = KNNImputer(n_neighbors=5, weights="uniform")
            temp = impute.fit_transform(data)
            data = pd.DataFrame(temp, columns=data.columns)
            self.logger.log(self.file, "Preprocessing : imputing null values Successfully")
            return data

        except Exception as e:
            self.logger.log(self.file, "Preprocessing : imputing null values Failure %s" % e)
            raise e

    def dropColwithZeroStd(self, data):

        try:
            data = pd.DataFrame(data)

            dic = data.describe()

            for i in data.columns:
                if dic[i]['std'] == 0:
                    data = data.drop([i], axis=1)
            self.logger.log(self.file, "Preprocessing : drop column with 0 std Successfully")
            return data

        except Exception as e:
            self.logger.log(self.file, "Preprocessing : drop column with 0 std Failure %s" % e)
            raise e
