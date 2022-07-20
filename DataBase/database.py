import sqlite3
from os import listdir
import csv
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


    def savetoDB(self,name):

        conn = self.createConn(name)


        onlyfiles = [f for f in listdir("Good_Raw_Files")]

        # for file in onlyfiles:
        #     try:
        #         with open("Good_Raw_Files/" + file, "r") as f:
        #             next(f)
        #             reader = csv.reader(f, delimiter="\n")
        #             for line in enumerate(reader):
        #                 for list_ in (line[1]):
        #
        #                     try:
        #                         conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=list_))
        #                         print("here")
        #                         conn.commit()
        #                     except Exception as e:
        #                         print("exception")
        #                         raise e
        #
        #     except Exception as e:
        #
        #         pass
        #
        # conn.close()
        for file in onlyfiles:

            with open("Good_Raw_Files/" + file, "r") as f:
                next(f)
                reader = csv.reader(f, delimiter="\n")
                for line in enumerate(reader):
                    for list_ in (line[1]):


                        conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=list_))
                        print("here")
                        conn.commit()



        conn.close()