import pandas as pd
from sklearn.cluster import KMeans
from kneed import KneeLocator
import matplotlib.pyplot as plt


class Clustering:

    def clustering(self):
        data = pd.read_csv("X.csv")
        k = self.findK(data)
        clustered_data = self.createClusters(data,k)
        list_of_clusters = clustered_data['cluster'].unique()

        return clustered_data,list_of_clusters

    def findK(self,data):

        wcss=[]

        for i in range(1,11):
            kmeans = KMeans(n_clusters=i,init="k-means++",random_state=101)
            kmeans.fit(data)

            wcss.append(kmeans.inertia_)

        plt.plot(range(1,11),wcss)
        plt.title("Values at K")
        plt.xlabel("k")
        plt.ylabel("wcss")
        plt.savefig("Clustering/plot.png")
        k = KneeLocator(range(1,11),wcss,curve="convex",direction="decreasing")

        return k.knee

    def createClusters(self,data,k):
        kmeans = KMeans(n_clusters=k, init="k-means++", random_state=101)
        kmeans = kmeans.fit_predict(data)
        data['cluster']=kmeans
        return data


