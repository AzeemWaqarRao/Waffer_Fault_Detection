import json
from os import listdir
import re
import shutil
import pandas as pd
import glob
import os

class Data_Validation:

    def __init__(self):
        self.schema_path = "Data_Validation/schema_training.json"
        self.path = "Training_Batch_Files"


    def getValuesFromSchema(self):
        f = open(self.schema_path,"r")
        dic = json.load(f)

        lengthOfDateStampInFile = dic['LengthOfDateStampInFile']
        lengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
        numberofColumns = dic['NumberofColumns']
        sampleFileName = dic['SampleFileName']
        column_names = dic["ColName"]

        return lengthOfTimeStampInFile, lengthOfDateStampInFile,numberofColumns,sampleFileName,column_names



    def manualRegexCreation(self):

        regex = "['wafer']+['\_']+[\d_]+[\d]+\.csv"
        return regex

    def validatefile(self,regex,lengthOfDateStampInFile,lengthOfTimeStampInFile):
        for filename in listdir(self.path):

            extension = filename.split(".")[1]
            if extension == "csv":

                name = filename.split(".")[0]
                name = name.split("_")

                if ((name[0]=="Wafer" or name[0]=="wafer") and len(name[1]) == lengthOfDateStampInFile and len(name[2])==lengthOfTimeStampInFile):

                    shutil.copy("Training_Batch_Files/" + filename, "Good_Raw_Files")
                else:
                    shutil.copy("Training_Batch_Files/" + filename, "Bad_Raw_Files")
            else:
                shutil.copy("Training_Batch_Files/" + filename, "Bad_Raw_Files")


    def validateColumn(self,numberofColumns):
        for file in listdir("Good_Raw_Files"):
            df = pd.read_csv("Good_Raw_Files/"+file)
            if numberofColumns == df.shape[1]:
                pass
            else:
                shutil.move("Good_Raw_Files/" + file, "Bad_Raw_Files")

    def validateMissingValuesInWholeColumn(self):

        try:


            for file in listdir('Good_Raw_Files'):
                csv = pd.read_csv("Good_Raw_Files/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("Good_Raw_Files/" + file,
                                    "Bad_Raw_Files")

                        break
                if count == 0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("Good_Raw_Files/" + file, index=None, header=True)
        except OSError:
           pass
        except Exception as e:
           pass


    def mergeFiles(self):


        files = os.path.join("Good_Raw_Files", "*.csv")


        files = glob.glob(files)

        df = pd.concat(map(pd.read_csv, files), ignore_index=True)
        df.iloc[:, 1:].to_csv("Training_Data.csv")


    def deleteRawFiles(self):

        dir = 'Good_Raw_Files'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        dir = 'Bad_Raw_Files'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

