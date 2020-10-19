import pandas as pd
import pyodbc

# Import CSV
data = pd.read_csv ('LuClinic.csv')   
df = pd.DataFrame(data, columns= ['col_1', 'col_2', 'col_3'])

# Connect to SQL Server
conn = pyodbc.connect(host='localhost',
                      port='8889',
                      database='LuClinic',
                      user='root',
                      password='root',
                      Trusted_Connection='yes')

cursor = conn.cursor()

# Create Table
cursor.execute('CREATE TABLE table_name (col_1 nvarchar(50), col_2 nvarchar(50), col_3 int)')

# Insert DataFrame to Table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO LuClinic.dbo.table_name (col_1, col_2, col_3)
                VALUES (?,?,?)
                ''',
                row.col_1, 
                row.col_2,
                row.col_3
                )
conn.commit()