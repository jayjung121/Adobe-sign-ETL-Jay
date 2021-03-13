import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta

default_args = {
    'owner': 'jay',
    'depends_on_past': False,
    'start_date': datetime(2019, 11,12),
    'email': ['ByungSuJ@seahawks.com', 'RileyM@Seahawks.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'email_on_success': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    # 'schedule_interval':'0 * * * *'
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('Adobe_Sign_Dag', default_args=default_args, schedule_interval='0 12 * * *')

adobe_sign_daily_command1 = "cd ~/airflow/dags/adobe-sign && python3 main.py"

# gameday_daily_command2 = 'source gameday_venv/bin/activate && cd gameday_venv/votf_ticket_member_2019'
# gameday_daily_command3 = 'python3 main.py'

t1 = BashOperator(
    task_id='daily_run1',
    bash_command=adobe_sign_daily_command1,
    dag=dag
)

# t2 = BashOperator(
#     task_id='daily_run2',
#     bash_command=gameday_daily_command2,
#     dag=dag
# )

# t3 = BashOperator(
#     task_id='daily_run3',
#     bash_command=gameday_daily_command3,
#     dag=dag
# )

success = EmailOperator (
    dag=dag,
    trigger_rule=TriggerRule.ALL_SUCCESS,
    task_id="task_success",
    to=["ByungSuJ@seahawks.com", 'RileyM@Seahawks.com'],
    subject='ADOBE SIGN pipline successfully processed. {{ ds }}',
    html_content='<h3>Daily run succeeded for ADOBE SIGN data pipeline </h3>'
    )

fail = EmailOperator (
    dag=dag,
    trigger_rule=TriggerRule.ONE_FAILED,
    task_id="task_failed",
    to=["ByungSuJ@seahawks.com", 'RileyM@Seahawks.com'],
    subject='ADOBE SIGN pipline process failed. {{ ds }}',
    html_content='<h3>Daily run Failed for ADOBE SIGN data pipeline</h3>'
    )

# ,html_content='<h3>daily run Failed for ABI data pipeline</h3>'
t1  >> [success, fail]
