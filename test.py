import os
from Data_Validation.validate_data import Data_Validation
from Transform_Data.transform_data import Transform_Data
from DataBase.database import dbOperartions
from Logger.logger import Logger

dir = 'Good_Raw_Files'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'Bad_Raw_Files'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))


dv = Data_Validation("E:\Github\Waffer_Fault_Detection\Training_Batch_Files",os.path.join("Data_Validation","schema_training.json"))

lengthOfTimeStampInFile, lengthOfDateStampInFile, numberofColumns, sampleFileName, column_names = dv.getValuesFromSchema()
dv.validatefile(lengthOfDateStampInFile,lengthOfTimeStampInFile)
dv.validateColumn(numberofColumns)
dv.validateMissingValuesInWholeColumn()