import sqlite3
from os import listdir
import csv

import pandas as pd


class dbOperartions:

    def createConn(self,name):

        try:
            conn = sqlite3.connect("DataBase/"+name+".db")

        except ConnectionError:

            raise ConnectionError

        return conn

    def createTable(self,dbname,column_names):

       try:
           conn = self.createConn(dbname)
           c = conn.cursor()
           c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
           if c.fetchone()[0]==1:
                pass
                #    table exists
           else:
               for key in column_names.keys():
                   type = column_names[key]

                   try:
                       c.execute("ALTER TABLE Good_Raw_Data ADD COLUMN '{}' {}".format(key,type))



                   except:
                       c.execute("CREATE TABLE Good_Raw_Data ('{}' '{}')".format(key,type))


           conn.close()







       except:
            pass


    def savetoDB(self,name,column_names):

        df = pd.read_csv("Training_Data.csv")

        df = df.iloc[:, 1:]
        df.columns = (list(column_names.keys()))


        conn = self.createConn(name)
        df.to_sql('Good_Raw_Data', conn, if_exists='append', index=False)

        c = conn.cursor()
        c.execute('SELECT * FROM Good_Raw_Data')
        conn.commit()
        conn.close()
