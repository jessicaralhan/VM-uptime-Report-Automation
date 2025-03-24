"""
I need a script or automation of some sorts which runs on a daily basis which gets me a list of
running instances (VMs) on a cloud provider. 

It should show me a report of the instances that are running for a certain period of time. 
(That time can be configurable eventually )

"""

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
import schedule
import time
from datetime import datetime
import pytz
import json 
import configparser
import boto3


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


def run_example():
  
    report_days, azure_creds, aws_creds = get_configuration()

    if azure_creds:
        credentials = ClientSecretCredential(
            client_secret=azure_creds['client_secret'],
            client_id=azure_creds['client_id'],
            tenant_id=azure_creds['tenant_id'],
            )
        compute_client = ComputeManagementClient(credentials, azure_creds['subscription_id'])
        day = datetime.today().strftime('%Y-%m-%d')
        dt = datetime.strptime(day, "%Y-%m-%d")
        timezone = pytz.UTC
        dt_with_timezone = timezone.localize(dt)
        info = []     
        try:
            for vm in compute_client.virtual_machines.list_all():
                if abs((vm.time_created - dt_with_timezone).days) >= int(report_days):
                    print(f"VM name which is running from last {report_days} or more than {report_days} days -", vm.name) 
                    id = vm.id
                    splitIDbyslash = id.split('/')
                    time_created = vm.time_created.strftime("%Y/%m/%d %H:%M")
                    if vm.os_profile.linux_configuration is not None:
                        osName = "linux"
                    elif vm.os_profile.windows_configuration is not None:
                        osName = "Window"
                    
                    vm_info = {
                        "VM Name": vm.name,
                        "VM ID": vm.id,
                        "VM Resource Group": splitIDbyslash[4],
                        "VM operating system": osName,
                        "VM Subscription ID": splitIDbyslash[2],
                        "Region": vm.location,
                        "VM type": vm.type,
                        "VM id" : vm.vm_id,
                        "Provisioning state": vm.provisioning_state,
                        "VM Launch Time": time_created
                        }
                    info.append(vm_info)
            file = open(f"{day}.json","a")
                    
            file.write(json.dumps(info))
            file.close()
            print("VM report is generated")
        except Exception as e:
            print(f"\nError: {e}")
    
    # List ec2 instances
    if aws_creds:
        ec2_client = boto3.client('ec2', aws_access_key_id=aws_creds['access_key'], aws_secret_access_key=aws_creds['secret_key'], region_name=aws_creds['region'])
        response = ec2_client.describe_instances()
        ec2_info = []
        day = datetime.today().strftime('%Y-%m-%d')
        try: 
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                        print("Running EC2 -",instance['Tags'][0]['Value'])
                        instance_id = instance['InstanceId']
                        instance_type = instance['InstanceType']
                        tags = instance['Tags'][0]['Value']
                        state = instance['State']['Name']
                        time = instance['LaunchTime']
                        launch_time = time.strftime("%Y/%m/%d %H:%M")
                        Region = instance['Placement']['AvailabilityZone']
                        instance_info = {
                            "VM Name": tags,
                            "VM ID": instance_id,
                            "VM Type": instance_type,
                            "Region": Region,
                            "VM State": state,
                            "VM Launch Time": launch_time
                        }
                        ec2_info.append(instance_info)
            file = open(f"{day}.json","a")
            file.write(json.dumps(ec2_info))
            file.close()
            print("EC2 report is generated")
            
                
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    schedule.every().day.at("18:00").do(run_example)
    while True:
        schedule.run_pending()
        time.sleep(1)


    




