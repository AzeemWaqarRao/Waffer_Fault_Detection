import os

import pandas
import pandas as pd
from Logger.logger import Logger
from File_Ops.file_ops import File_Ops

class Predict_Result:

    def __init__(self):
        self.path = "Prediction_Data.csv"
        self.file_ops = File_Ops()
        self.logger = Logger()
        self.file = open(os.path.join("Prediction_Logs", "findingPrediction.txt"), mode='a+')


    def predict(self):

        try:
            self.logger.log(self.file,"Prediction Started")
            kmeans = self.file_ops.load_model("kmeans")
            self.logger.log(self.file,"Kmeans Loaded")

            data = pd.read_csv(self.path)

            cluster = kmeans.predict(data.drop(['Wafer'], axis=1))
            data['cluster'] = cluster

            clusters = data['cluster'].unique()

            for i in clusters:
                self.logger.log(self.file, "Prediction Started for cluster "+str(i))

                cluster_data = data[data['cluster'] == i]
                wafer = list(cluster_data['Wafer'])

                cluster_data = cluster_data.drop(['Wafer', 'cluster'], axis=1)
                model_name = self.file_ops.find_model(i)
                model = self.file_ops.load_model(model_name)
                self.logger.log(self.file, "Model Loaded : "+str(model_name))
                self.logger.log(self.file, "Computation Started")

                prediction = list(model.predict(cluster_data))
                result = pandas.DataFrame(list(zip(wafer, prediction)), columns=['Wafer', 'Prediction'])
                self.logger.log(self.file, "Computation Completed")

                result.to_csv("Predict_Result/prediction.csv", mode="a+", header=True)
                self.logger.log(self.file, "Prediction cluster "+str(i)+" stored in prediction.csv ")

        except Exception as e:

            self.logger.log(self.file, "Exception While Predicting Results " + str(e))
            raise e

        self.logger.log(self.file, "Prediction Completed")
        self.file.close()





