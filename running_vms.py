from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
import os
import schedule
import time


LOCATION = 'us-east-1'

# Resource Group
GROUP_NAME = 'py-assignment-1'

def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ClientSecretCredential(
        client_secret=os.environ['AZURE_CLIENT_SECRET'],
        client_id=os.environ['AZURE_CLIENT_ID'],
        tenant_id=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id


def run_example():
    
    # Create all clients with an Application (service principal) token provider
    credentials, subscription_id = get_credentials()
    compute_client = ComputeManagementClient(credentials, subscription_id)

    try:
        # List VMs in subscription
        print('\nList VMs in subscription')
        for vm in compute_client.virtual_machines.list_all():
            print("\tVM: {}".format(vm.name))

        # List VM in resource group
        print('\nList VMs in resource group')
        for vm in compute_client.virtual_machines.list(GROUP_NAME):
            print("\tVM: {}".format(vm.name))
         
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    schedule.every().day.at("18:00").do(run_example)

    while True:
        schedule.run_pending()
        time.sleep(1)













