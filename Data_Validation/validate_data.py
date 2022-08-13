import json
import sys
from os import listdir
import re
import shutil
import pandas as pd
import glob
import os
from Logger.logger import Logger

class Data_Validation:

    def __init__(self,path,schema_path):
        self.schema_path = schema_path
        self.path = path
        self.logger = Logger()


    def getValuesFromSchema(self):
        try:
            f = open(self.schema_path, "r")
            dic = json.load(f)
            f.close()

            lengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            lengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            numberofColumns = dic['NumberofColumns']
            sampleFileName = dic['SampleFileName']
            column_names = dic["ColName"]
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message = "LengthOfDateStampInFile:: %s" % lengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % lengthOfTimeStampInFile + "\t " + "NumberofColumns:: %s" % numberofColumns + "\n"
            self.logger.log(file, message)

            file.close()

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file,"ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return lengthOfTimeStampInFile, lengthOfDateStampInFile,numberofColumns,sampleFileName,column_names



    def manualRegexCreation(self):

        regex = "['wafer']+['\_']+[\d_]+[\d]+\.csv"
        return regex

    def validatefile(self,lengthOfDateStampInFile,lengthOfTimeStampInFile):

        try:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')

            for filename in listdir(self.path):

                extension = filename.split(".")[1]
                if extension == "csv":

                    name = filename.split(".")[0]
                    name = name.split("_")

                    if ((name[0] == "Wafer" or name[0] == "wafer") and len(name[1]) == lengthOfDateStampInFile and len(
                            name[2]) == lengthOfTimeStampInFile):

                        shutil.copy(os.path.join(self.path, filename), "Good_Raw_Files")
                        self.logger.log(f, "Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                    else:
                        shutil.copy(os.path.join(self.path, filename), "Bad_Raw_Files")
                        self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

                else:
                    shutil.copy(os.path.join(self.path, filename), "Bad_Raw_Files")
                    self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
            f.close()

        except Exception as e:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')
            self.logger.log(f, "Error occured while validating FileName %s" % e)
            f.close()
            raise e




    def validateColumn(self,numberofColumns):

        try:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Column Length Validation Started!!")
            for file in listdir("Good_Raw_Files"):
                df = pd.read_csv("Good_Raw_Files/" + file)
                print("validate column")
                print(numberofColumns)
                print(df.shape[1])

                if numberofColumns == df.shape[1]:

                    self.logger.log(f, "Valid file!! :: %s" % file)

                else:
                    shutil.move("Good_Raw_Files/" + file, "Bad_Raw_Files")
                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)



        except OSError:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError

        except Exception as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e

        f.close()


    def validateMissingValuesInWholeColumn(self):

        try:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Missing Values Validation Started!!")

            for file in listdir('Good_Raw_Files'):
                csv = pd.read_csv("Good_Raw_Files/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("Good_Raw_Files/" + file,
                                    "Bad_Raw_Files")
                        self.logger.log(f,"Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)


                        break
                if count == 0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("Good_Raw_Files/" + file, index=None, header=True)
        except OSError:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError

        except Exception as e:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e

    def mergeFiles(self,filename):

        try:
            f = open("Training_Logs/Training_Logs_General.txt", 'a+')
            files = os.path.join("Good_Raw_Files", "*.csv")

            files = glob.glob(files)

            df = pd.concat(map(pd.read_csv, files), ignore_index=True)
            self.logger.log(f, "Training Batch Files Merged")
            df.iloc[:, 1:].to_csv(filename + ".csv")
            self.logger.log(f, "Training Batch Files exported to CSV")
            f.close()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            self.logger.log(f, "Error Occured:: %s" % e)
            self.logger.log(f, str(exc_type) +" "+ str(fname)+" "+ str(exc_tb.tb_lineno))
            f.close()
            raise e




    def deleteRawFiles(self):

        try:
            dir = 'Good_Raw_Files'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            dir = 'Bad_Raw_Files'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

        except Exception as e:
            f = open("Training_Logs/Training_Logs_General.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e



