import sqlite3
import pandas as pd
import os

# Connect to the SQLite database
data = input("Enter the name of the database: ")
conn = sqlite3.connect(f"{data}.db")

# Fetch all table names from the database
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()

# Create an Excel writer object
excel_file = f"{data}.xlsx"
if os.path.exists(excel_file):
    os.remove(excel_file)

excel_writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")

# Iterate over each table and write its contents to the Excel file
for table_name in table_names:
    # Read table data into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name[0]}", conn)
    
    # Write DataFrame to Excel sheet
    df.to_excel(excel_writer, sheet_name=table_name[0], index=False)

# Save and close the Excel file
excel_writer._save()
excel_writer.close()

# Close the database connection
conn.close()

print("Data exported successfully to Excel.")

