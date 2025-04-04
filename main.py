"""
I need a script or automation of some sorts which runs on a daily basis which gets me a list of
running instances (VMs) on a cloud provider. 

It should show me a report of the instances that are running for a certain period of time. 
(That time can be configurable eventually )

"""

import logging
import configparser
from azure_helper import azure_report
from aws_helper import aws_report
import time
from gcp_helper import gcp_report
from dotenv import load_dotenv
import os
import schedule

load_dotenv()

service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_configuration():
    '''
        Configuration function which is reading from config.ini sections to get the credentials for AWS and AZURE 
    '''
    config = configparser.ConfigParser()
    config.read('test_config.ini')

    try:
        if 'AZURE' in config.sections():
            subscription_id = config['AZURE']['SUBSCRIPTION_ID']
            client_secret = config['AZURE']['CLIENT_SECRET']
            client_id = config['AZURE']['CLIENT_ID']
            tenant_id = config['AZURE']['TENANT_ID']
            azure_credentials = {
                "subscription_id": subscription_id,
                "client_secret": client_secret,
                "client_id": client_id,
                "tenant_id": tenant_id,
            }
            aws_credentials = None
        elif 'AWS' in config.sections():
            access_key = config['AWS']['ACCESS_KEY']    
            secret_key = config['AWS']['SECRET_KEY']
            region = config['AWS']['REGION']
            aws_credentials = {
                "access_key": access_key,
                "secret_key": secret_key,
                "region": region,
            }     
            azure_credentials = None
        elif 'GCP' in config.sections():
            project_id = config['GCP']['PROJECT_ID']
            client_id = config['GCP']['CLIENT_ID']
            token_uri = config['GCP']['TOKEN_URI']
            client_email = config['GCP']['CLIENT_EMAIL']
            auth_uri = config['GCP']['AUTH_URI']
            gcp_credentials = {
                "project_id": project_id,
                "client_id": client_id,
                "token_uri": token_uri,
                "client_email": client_email,
                "auth_uri": auth_uri
            }
            azure_credentials = None
            aws_credentials = None
        else:
            raise Exception("AWS, GCP and AZURE both are not present in config.ini file")

    except Exception as e:
        logger.error("Credentials error. Recheck the credentials", exc_info=True)
        return None, None, None

    report_days = config['REPORT']['DAYS']
    return report_days, azure_credentials, aws_credentials, gcp_credentials


def running_vms():
    '''
    Running the code to get the report for running VMs
    '''
    report_days, azure_creds, aws_creds, gcp_creds = get_configuration()
    if azure_creds:
        azure_report(report_days, azure_creds, logger)
    if aws_creds:
        aws_report(aws_creds, report_days, logger)
    if gcp_creds:
        project_id = gcp_creds["project_id"]
        logger.info(f"Fetching GCP instances for project: {project_id}")
        gcp_report(project_id, logger)


if __name__ == "__main__":
    schedule.every().day.at("18:00").do(running_vms)
    while True:
        schedule.run_pending()
        time.sleep(1)


