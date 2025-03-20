"""
I need a script or automation of some sorts which runs on a daily basis which gets me a list of
running instances (VMs) on a cloud provider. 

It should show me a report of the instances that are running for a certain period of time. 
(That time can be configurable eventually )

"""

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
import os
import schedule
import time
from datetime import datetime
import pytz
import json 
import configparser

def get_credentials():
    config = configparser.ConfigParser()
    config.read('test_config.ini')

    subscription_id = config['AZURE']['SUBSCRIPTION_ID']
    client_secret = config['AZURE']['CLIENT_SECRET']
    client_id = config['AZURE']['CLIENT_ID']
    tenant_id = config['AZURE']['TENANT_ID']
   
    report_days = config['REPORT']['DAYS']

    credentials = ClientSecretCredential(
        client_secret=client_secret,
        client_id=client_id,
        tenant_id=tenant_id
    )
    
    return credentials, subscription_id, report_days

def run_example():
    
    # Create all clients with an Application (service principal) token provider
    credentials, subscription_id, report_days = get_credentials()
    compute_client = ComputeManagementClient(credentials, subscription_id)
    day = datetime.today().strftime('%Y-%m-%d')
    dt = datetime.strptime(day, "%Y-%m-%d")
    timezone = pytz.UTC
    dt_with_timezone = timezone.localize(dt)
    info = []

    try:
        # List VM in subscription
        
        print('\nList VMs in subscription -')
        for vm in compute_client.virtual_machines.list_all():
            if abs((vm.time_created - dt_with_timezone).days) >= int(report_days):
                print(f"VM name which is running from last {report_days} or more than {report_days} days -", vm.name) 
                id = vm.id
                splitIDbyslash = id.split('/')
                time_created = vm.time_created.strftime("%Y/%m/%d %H:%M")
                # print("os profile",vm.os_profile.linux_configuration)
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
                    "VM time_created": time_created
                    }
                info.append(vm_info)
        file = open(f"{day}.json","a")
                
        file.write(json.dumps(info))
        file.close()
        print("Report is generated")
    except Exception as e:
        print(f"\nError: {e}")
     

if __name__ == "__main__":
    schedule.every().day.at("18:00").do(run_example)
    while True:
        schedule.run_pending()
        time.sleep(1)


    




