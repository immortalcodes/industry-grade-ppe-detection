import psycopg2
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_database(database, user, password, host="localhost", port="5432"):
    try:
        connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        cursor = connection.cursor()
        print("Connected to database successfully.")
        return connection, cursor
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        return None, None

def close_database_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("Connection to database closed.")

def pandas_df_to_pdf(dataframe, output_file):
    try:
        with PdfPages(output_file) as pdf:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.axis('tight')
            ax.axis('off')
            ax.table(cellText=dataframe.values, colLabels=dataframe.columns, cellLoc='center', loc='center')
            pdf.savefig()
            plt.close()
        print("PDF file created successfully.")
    except Exception as e:
        print("Error creating PDF file:", e)

