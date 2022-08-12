import os
from Data_Validation.validate_data import Data_Validation
from Transform_Data.transform_data import Transform_Data
from DataBase.database import dbOperartions
from Logger.logger import Logger

class Training_Validation:

    def __init__(self,path):
        self.path = path
        self.schema_path = os.path.join("Data_Validation","schema_training.json")
        self.dv = Data_Validation(self.path,self.schema_path)
        self.td = Transform_Data()
        self.db = dbOperartions()
        self.dv.deleteRawFiles()
        self.logger = Logger()
        self.file = open(os.path.join("Training_Logs","Training_Logs_General.txt"),mode='a+')


    def validate_data(self):

        self.logger.log(self.file,"Training Validation Started.")
        lengthOfTimeStampInFile, lengthOfDateStampInFile,numberofColumns,sampleFileName,column_names = self.dv.getValuesFromSchema()

        self.dv.validatefile(lengthOfDateStampInFile,lengthOfTimeStampInFile)
        self.dv.validateColumn(numberofColumns)
        self.dv.validateMissingValuesInWholeColumn()
        self.logger.log(self.file, "Training Validation Completed.")

        self.td.putNull()
        self.dv.mergeFiles("Training_Data")
        self.logger.log(self.file, "Training Preprocessing Completed.")
        self.db.createTable("Training_Data",column_names)
        self.logger.log(self.file, "DataBase Created.")
        self.db.savetoDB("Training_Data",column_names,"Training_Data.csv")
        self.logger.log(self.file, "Training Data stored to DataBase.")
        self.dv.deleteRawFiles()
        self.logger.log(self.file, "Raw Files Deleted.")






