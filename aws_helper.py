from datetime import datetime
import boto3
import json
import pytz

def aws_report(aws_creds, report_days):
        ec2_client = boto3.client('ec2', aws_access_key_id=aws_creds['access_key'], aws_secret_access_key=aws_creds['secret_key'], region_name=aws_creds['region'])
        response = ec2_client.describe_instances()
        ec2_info = []
        day = datetime.today().strftime('%Y-%m-%d')
        dt = datetime.strptime(day, "%Y-%m-%d")
        timezone = pytz.UTC
        dt_with_timezone = timezone.localize(dt)
        try: 
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if abs((instance['LaunchTime'] - dt_with_timezone).days) >= int(report_days):
                        instance_name = instance['Tags'][0]['Value']
                        print(f"VM name which is running from last {report_days} or more than {report_days} days -", instance_name)
                        print("Running EC2 -",instance['Tags'][0]['Value'])
                        instance_id = instance['InstanceId']
                        instance_type = instance['InstanceType']
                        state = instance['State']['Name']
                        time = instance['LaunchTime']
                        launch_time = time.strftime("%Y/%m/%d %H:%M")
                        Region = instance['Placement']['AvailabilityZone']
                        instance_info = {
                            "VM Name": instance_name,
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