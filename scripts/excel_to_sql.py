import sqlite3
import pandas as pd


data = input("What is the name of the database ? ")
# Connect to the SQLite database
conn = sqlite3.connect(f'{data}.db')

# Read the Excel file
excel_file = f'{data}.xlsx'
df = pd.read_excel(excel_file)

# Get the table name (assuming it's the first sheet name)
table_name = pd.ExcelFile(excel_file).sheet_names[0]

# Delete existing data in the table
delete_query = f"DELETE FROM {table_name}"
conn.execute(delete_query)

# Insert the data from the Excel file into the table
df.to_sql(table_name, conn, if_exists='append', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data updated successfully in the database.")

