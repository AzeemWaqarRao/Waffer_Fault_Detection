import pandas as pd
import sqlite3
from Data_Validation.validate_data import Data_Validation
dv = Data_Validation()

conn = sqlite3.connect('DataBase/Training_Data.db')


c = conn.cursor()
c.execute('SELECT * FROM Good_Raw_Data')
conn.commit()
print(c.fetchall())