import os

import pandas as pd
from sklearn.cluster import KMeans
from kneed import KneeLocator
import matplotlib.pyplot as plt
from File_Ops.file_ops import File_Ops
from Logger.logger import Logger

class Clustering:

    def __init__(self):
        self.logger = Logger()
        self.file = open(os.path.join("Training_Logs", "clustering_training.txt"), mode='a+')

    def clustering(self):

        try:
            self.logger.log(self.file, "Clustering Started!")
            data = pd.read_csv("X.csv")
            k = self.findK(data)
            clustered_data = self.createClusters(data, k)
            list_of_clusters = clustered_data['cluster'].unique()
            self.logger.log(self.file, "Clustering Completed!")
            self.file.close()
            return clustered_data, list_of_clusters
        except Exception as e:
            self.logger.log(self.file,"Clustering: Exception Occurred "+str(e))
            raise e

    def findK(self,data):

        try:
            wcss = []

            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init="k-means++", random_state=101)
                kmeans.fit(data)

                wcss.append(kmeans.inertia_)

            plt.plot(range(1, 11), wcss)
            plt.title("Values at K")
            plt.xlabel("k")
            plt.ylabel("wcss")
            plt.savefig("Clustering/plot.png")
            k = KneeLocator(range(1, 11), wcss, curve="convex", direction="decreasing")
            self.logger.log(self.file, "optimum value of k is : " + str(k.knee))
            return k.knee

        except Exception as e:
            self.logger.log(self.file, "Finding K: Exception Occurred " + str(e))
            raise e

    def createClusters(self,data,k):

        try:
            kmeans = KMeans(n_clusters=k, init="k-means++", random_state=101)

            kmeans_values = kmeans.fit_predict(data)
            self.logger.log(self.file, "Clusters Created!")

            data['cluster'] = kmeans_values
            file_ops = File_Ops()
            file_ops.save_model(kmeans, "kmeans")
            self.logger.log(self.file, "Kmeans Trained Model Saved!")
            return data

        except Exception as e:
            self.logger.log(self.file, "Creating Clustering: Exception Occurred "+str(e))
            raise e



