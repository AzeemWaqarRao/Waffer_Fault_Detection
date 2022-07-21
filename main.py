import pandas as pd

from Training_Validation.training_validation import Training_Validation
from Model.preprocessing import Preprocessor
from Clustering.clustering import Clustering
from Model.model_finder import Model_Finder
import os



dir = 'Good_Raw_Files'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'Bad_Raw_Files'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))


tv = Training_Validation()
tv.validate_data()

pr = Preprocessor()
pr.preprocess()

cl = Clustering()
X , list_of_clusters = cl.clustering()
print(list_of_clusters)

X['label'] = pd.read_csv("y.csv").iloc[:,1:]

model_finder = Model_Finder(X,list_of_clusters)
model_finder.get_model()



