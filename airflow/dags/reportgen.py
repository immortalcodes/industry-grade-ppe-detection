from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from helpers.dbcon import pandas_df_to_pdf
class DatabaseConnector:
    def __init__(self, database, user, password, host="localhost", port="5432"):
        self.database = "ppe_detection"
        self.user = "admin"
        self.password = "admin1234"
        self.host = "localhost"
        self.port = 5432

    def connect(self):
        try:
            self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
            self.cursor = self.connection.cursor()
            print("Connected to database successfully.")
        except psycopg2.Error as e:
            print("Error connecting to database:", e)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Connection to database closed.")

class DataDumper:
    def __init__(self, connector):
        self.connector = connector

    def dump_data(self):
        self.connector.connect()

        self.connector.cursor.execute("SELECT * FROM continous_track")
        w_data = self.connector.cursor.fetchall()
        w_df = pd.DataFrame(w_data, columns=['id', 'feed_instance', 'position', 'timestamp'])
        w_df.to_csv('reports/w_data.csv', index=False)

        self.connector.cursor.execute("SELECT * FROM ppe_detection_results")
        ppe_data = self.connector.cursor.fetchall()
        ppe_df = pd.DataFrame(ppe_data, columns=['id', 'deep_track_id', 'detection_time', 'helmet_detected', 'vest_detected'])
        ppe_df.to_csv('reports/ppe_detection_data.csv', index=False)

        self.connector.close_connection()

class DataProcessor:
    def __init__(self, connector):
        self.connector = connector

    def process_data(self):
        w_df = pd.read_csv('reports/w_data.csv')
        ppe_df = pd.read_csv('reports/ppe_detection_data.csv')

        total_workers = len(w_df)
        total_helmet_detected = ppe_df['helmet_detected'].sum()
        total_vest_detected = ppe_df['vest_detected'].sum()
        ppe_compliance_rate = ((total_helmet_detected + total_vest_detected ) / total_workers) * 100

        metrics_df = pd.DataFrame({
            'date': [datetime.now().date()],
            'total_workers': [total_workers],
            'total_helmet_detected': [total_helmet_detected],
            'total_vest_detected': [total_vest_detected],
            'ppe_compliance_rate': [ppe_compliance_rate]
        })

        self.connector.connect()
        self.connector.cursor.executemany("INSERT INTO metrics (date, total_workers, ...) VALUES (%s, %s, ...)", metrics_df.values)
        self.connector.close_connection()

class ReportGenerator:
    def __init__(self, connector):
        self.connector = connector

    def generate_reports(self):
        self.connector.connect()
        self.connector.execute("SELECT * FROM metrics")
        metrics_data = self.cursor.fetchall()
        metrics_df = pd.DataFrame(metrics_data, columns=['date', 'total_workers', ...])

        pandas_df_to_pdf(metrics_df, 'reports/output.pdf')
        with PdfPages('reports/output.pdf') as pdf:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.axis('tight')
            ax.axis('off')
            ax.table(cellText=metrics_df.values, colLabels=metrics_df.columns, cellLoc='center', loc='center')
            pdf.savefig()
            plt.close()

        self.connector.close_connection()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('ppe_safety_detection_workflow', default_args=default_args, schedule_interval=timedelta(days=1))

connector = DatabaseConnector(database='ppe_detection', user='admin', password='admin1234')

task_dump_data = PythonOperator(
    task_id='dump_data_from_database',
    python_callable=DataDumper(connector).dump_data,
    dag=dag
)

task_process_data = PythonOperator(
    task_id='process_data_dump',
    python_callable=DataProcessor(connector).process_data,
    dag=dag
)

task_generate_reports = PythonOperator(
    task_id='generate_reports',
    python_callable=ReportGenerator(connector).generate_reports,
    dag=dag
)

task_dump_data >> task_process_data >> task_generate_reports
