## **Daily VM Uptime Report Automation**

Automated script which runs on a daily basis and gets a list a running instances(VMs) from cloud provider Azure/AWS and generates a report.

### **Pre-requisties**
- python
- pip
- venv 

### **To run this script**

1. Clone the repository 
``` 
git clone https://github.com/jessicaralhan/azure-SDK-learn.git 
```
2. Install the dependencies using pip.
```
pip install azure-identity
pip install azure-mgmt-compute
pip install schedule
pip install DateTime
pip install pytz
pip install jsonlib
pip install configparser
```
3. Run the code with 
```
python3 {file_name}
```
Get credentials from AZURE and AWS portal 

### **Configuration** 
In test_config.ini file if you want generate a report of AWS VMs then set the credentials of AWS and remove the AZURE section and vice versa.

**AZURE credentials**
```
SUBSCRIPTION_ID = <SUBSCRIPTION_ID>
CLIENT_SECRET = <CLIENT_SECRET>
CLIENT_ID = <CLIENT_ID>
TENANT_ID = <TENANT_ID>
```
You can get SUBSCRIPTION_ID, CLIENT_ID, TENANT_ID by logging into Azure Portal and following are the steps to get CLIENT_SECRET.
1) Login to the Azure Portal
2) Navigate to Azure Active Directory
3) Select App Registrations, locate the Azure AD App that you're trying to find the Client ID and Client Secret Key for
4) Within the Azure AD App, select Certificates & Secrets 

**AWS credentials**
```
ACCESS_KEY = <ACCESS_KEY>
SECRET_KEY = <SECRET_KEY>
REGION = <AWS_REGION>
```
To get AWS access key and secret key follow this [link](https://www.msp360.com/resources/blog/how-to-find-your-aws-access-key-id-and-secret-access-key/#:~:text=1%20Go%20to%20Amazon%20Web,and%20Secret%20Access%20Key%20option.)

### **Scheduling the Script**
   Set up Task Scheduler to run the script daily. Schedule the script to run every day at 8 AM:

### **Logging**
   Added logging so that users can track the execution and detect the errors in a log file you can check the application.log file. 

