import sqlite3
from os import listdir
import csv
import os
from Logger.logger import Logger

import pandas as pd


class dbOperartions:

    def __init__(self):
        self.logger = Logger()

    def createConn(self,name):

        self.file = open(os.path.join("Training_Logs","DBconnection_log.txt"),mode='a+')

        try:
            conn = sqlite3.connect(os.path.join("DataBase", name + ".db"))
            self.logger.log(self.file, "DataBase %s connection Established" % name)

        except ConnectionError:
            self.logger.log(self.file, "DataBase %s connection Failed" % name)
            raise ConnectionError
        self.file.close()
        return conn

    def createTable(self,dbname,column_names):

       try:
           conn = self.createConn(dbname)
           c = conn.cursor()
           c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
           if c.fetchone()[0]==1:
                conn.close()
                self.file = open(os.path.join("Training_Logs", "DBtablecreation_log.txt"), mode='a+')
                self.logger.log(self.file, "Table Already Exists")
                self.file.close()
                #    table exists
           else:
               for key in column_names.keys():
                   type = column_names[key]

                   try:
                       c.execute("ALTER TABLE Good_Raw_Data ADD COLUMN '{}' {}".format(key,type))



                   except:
                       c.execute("CREATE TABLE Good_Raw_Data ('{}' '{}')".format(key,type))

               self.file = open(os.path.join("Training_Logs", "DBtablecreation_log.txt"), mode='a+')
               self.logger.log(self.file, "Table Created")
               self.file.close()
           conn.close()

       except Exception as e:
           self.file = open(os.path.join("Training_Logs", "DBtablecreation_log.txt"), mode='a+')
           self.logger.log(self.file, "Error While Creating Table")
           self.file.close()
           raise e


    def savetoDB(self,name,column_names,filename):

        log_file = open("Training_Logs/DbInsertLog.txt", 'a+')
        try:
            df = pd.read_csv(filename)

            df = df.iloc[:, 1:]
            df.columns = (list(column_names.keys()))

            conn = self.createConn(name)
            df.to_sql('Good_Raw_Data', conn, if_exists='append', index=False)
            self.logger.log(log_file,"Data insertion completed")

            c = conn.cursor()
            c.execute('SELECT * FROM Good_Raw_Data')
            conn.commit()
            conn.close()

        except Exception as e:
            conn.rollback()
            self.logger.log(log_file,"Data insertion failed")
            conn.commit()
            conn.close()
        log_file.close()


