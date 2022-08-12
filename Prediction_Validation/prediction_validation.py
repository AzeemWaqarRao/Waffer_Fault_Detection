from Data_Validation.validate_data import Data_Validation
from Transform_Data.transform_data import Transform_Data
from DataBase.database import dbOperartions
import os
from Logger.logger import Logger

class Prediction_Validation:

    def __init__(self,path):
        self.path = path
        self.schema_path = os.path.join("Schema","schema_prediction.json")
        self.dv = Data_Validation(self.path,self.schema_path)
        self.td = Transform_Data()
        self.db = dbOperartions()
        self.dv.deleteRawFiles()
        self.logger = Logger()
        self.file = open(os.path.join("Prediction_Logs", "Prediction_Logs_General.txt"), mode='a+')


    def validate_data(self):


        self.logger.log(self.file,"Prediction Validation Started.")

        lengthOfTimeStampInFile, lengthOfDateStampInFile, numberofColumns, sampleFileName, column_names\
            = self.dv.getValuesFromSchema()
        self.dv.validatefile(lengthOfDateStampInFile, lengthOfTimeStampInFile)
        self.dv.validateColumn(numberofColumns)
        self.dv.validateMissingValuesInWholeColumn()
        self.logger.log(self.file, "Prediction Validation Completed.")


        self.td.putNull()
        self.dv.mergeFiles("Prediction_Data")
        self.logger.log(self.file, "Prediction Preprocessing Completed.")
        self.db.createTable("Prediction_Data", column_names)
        self.logger.log(self.file, "DataBase Created.")
        self.db.savetoDB("Prediction_Data", column_names, "Prediction_Data.csv")
        self.logger.log(self.file, "Prediction Data stored to DataBase.")
        self.dv.deleteRawFiles()
        self.logger.log(self.file, "Raw Files Deleted.")

