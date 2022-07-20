from os import listdir
import pandas as pd

class Transform_Data:


    def putNull(self):
        for file in listdir("Good_Raw_Files"):
            df = pd.read_csv("Good_Raw_Files/" + file)
            df.fillna("Null",inplace=True)

            df.to_csv("Good_Raw_Files/"+file)
