import sys

sys.path.append("/home/jmiller/git/AFDTools")
from datetime import datetime, timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


args = dict(
    {
        "owner": "airflow",
        "start_date": airflow.utils.dates.days_ago(1),
        "email": ["jj.miller.jm@gmail.com"],
        "email_on_failure": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=10),
    }
)

dag = DAG(
    dag_id="AFD_Workflow", schedule_interval="@hourly", default_args=args
)

###############################################################


def getForecast():
    """
    """
    from forecast import Downloader

    with open('data/offices.txt', 'r') as t:
        OFFICES = t.readlines()

    for office in OFFICES:
        try:
            d = Downloader(office.strip())
            forecast = d.download()
            d.insert(forecast)
        except:
            pass


grabForecast = PythonOperator(
    task_id="grab_forecast", python_callable=getForecast, dag=dag
)

###############################################################


def getPhrases():
    """
    """
    from extract import Extract

    ex = Extract()
    ex.run()


getPhrases = PythonOperator(
    task_id="get_phrases", python_callable=getPhrases, dag=dag
)

###############################################################


def phrases2Dataset():
    """
    """
    from dataset import Dataset

    d = Dataset()
    d.add2Dataset(total=1000)


add2Dataset = PythonOperator(
    task_id="add_to_dataset", python_callable=phrases2Dataset, dag=dag
)

###############################################################

grabForecast >> getPhrases >> add2Dataset
