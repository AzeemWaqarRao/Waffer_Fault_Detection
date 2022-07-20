import csv
from os import listdir
import pandas as pd
import sqlite3


# onlyfiles = [f for f in listdir("Good_Raw_Files")]
# for file in onlyfiles:
#
#     with open("Good_Raw_Files/" + file, "r") as f:
#         next(f)
#         reader = csv.reader(f, delimiter="\n")
#         for line in enumerate(reader):
#             for list_ in (line[1]):
#                pass
# print(list_)
conn = sqlite3.connect("DataBase/Training_Data.db")
c = conn.cursor()




for file in listdir("Good_Raw_Files"):
    df = pd.read_csv("Good_Raw_Files/"+file)

a = (list(df.iloc[1,1:]))
df = (df.iloc[1,1:])
print(a)


c.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=df))
conn.commit()
c.execute("SELECT * FROM Good_Raw_Data")
print(c.fetchall())
