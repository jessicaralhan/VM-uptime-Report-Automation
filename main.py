"""
I need a script or automation of some sorts which runs on a daily basis which gets me a list of
running instances (VMs) on a cloud provider. 

It should show me a report of the instances that are running for a certain period of time. 
(That time can be configurable eventually )

"""

import schedule
import time
import configparser
from azure_helper import azure_report
from aws_helper import aws_report

def get_configuration():
    config = configparser.ConfigParser()
    config.read('test_config.ini')
    try:
        if 'AZURE' in config:
            subscription_id = config['AZURE']['SUBSCRIPTION_ID']
            client_secret = config['AZURE']['CLIENT_SECRET']
            client_id = config['AZURE']['CLIENT_ID']
            tenant_id = config['AZURE']['TENANT_ID']
            azure_credentials = {
                "subscription_id":subscription_id,
                "client_secret":client_secret,
                "client_id":client_id,
                "tenant_id":tenant_id,
            }
            aws_credentials = None
        elif 'AWS' in config:
            access_key = config['AWS']['ACCESS_KEY']
            secret_key = config['AWS']['SECRET_KEY']
            region = config['AWS']['REGION']
            aws_credentials = {
                "access_key": access_key,
                "secret_key": secret_key,
                "region": region,
            }     
            azure_credentials = None
    except Exception as e:
        print("error", e)
        
    report_days = config['REPORT']['DAYS']

    return report_days, azure_credentials, aws_credentials

def running_vms():
    report_days, azure_creds, aws_creds = get_configuration()
    if azure_creds:
        azure_report(report_days, azure_creds)
    if aws_creds:
        aws_report(aws_creds, report_days)


if __name__ == "__main__":
    schedule.every().day.at("18:00").do(running_vms)
    while True:
        schedule.run_pending()
        time.sleep(1)


