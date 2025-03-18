"""
I need a script or automation of some sorts which runs on a daily basis which gets me a list of
running instances (VMs) on a cloud provider. 

It should show me a report of the instances that are running for a certain period of time. 
(That time can be configurable eventually )
Anybody who has bandwidth from their projects can you pick this up?
Before you start implementing please setup a 1:1 with me where we can go over the plan of implementation for the same. 
I would like to understand how you would solve this.

"""
import schedule
import time

def print_message():
    print("Task executed at:", time.strftime("%H:%M:%S"))

schedule.every().day.at("18:00").do(print_message)

# Keep the program running to allow scheduled tasks to execute
while True:
    schedule.run_pending()
    time.sleep(1)