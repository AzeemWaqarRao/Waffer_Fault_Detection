import os.path
from os import listdir
import pandas as pd
from Logger.logger import Logger

class Transform_Data:

    def __init__(self):
        self.logger = Logger()
        self.file = open(os.path.join("Training_Logs","trainingPreprocessingLogs.txt"),mode='a+')


    def putNull(self):
        try:
            for file in listdir("Good_Raw_Files"):
                df = pd.read_csv("Good_Raw_Files/" + file)
                df.fillna("NULL", inplace=True)

                df.to_csv("Good_Raw_Files/" + file)
                self.logger.log(self.file,"Null values added in file :: %s" % file)

        except Exception as e:

            self.logger.log(self.file, "Error Occured:: %s" % e)
            f.close()
            raise e

