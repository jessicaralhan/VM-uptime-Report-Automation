***Daily VM Uptime Report Automation***

Automated report which runs on a daily basis and getting a list a running instances(VMs) from cloud provider(Azure). 

***Running this sample***
1. If you don't already have it, install Python.
2. General recommendation for Python development is to use a Virtual Environment. For more information, see https://docs.python.org/3/tutorial/venv.html

Install and initialize the virtual environment with the "venv" module on Python 3
```
python -m venv mytestenv # Might be "python3" or "py -3.6" depending on your Python installation
cd mytestenv
source bin/activate      # Linux shells (Bash, ZSH, etc.)
scripts\activate         # Windows shells (PowerShell, CMD)
```
3. Clone the repository 
``` 
git clone https://github.com/jessicaralhan/azure-SDK-learn.git 
```
4. Install the dependencies using pip.
```
pip install azure-identity
pip install azure-mgmt-compute
pip install schedule
pip install DateTime
pip install pytz
pip install jsonlib
pip install configparser
```
4. Run the code with 
```
python3 {file_name}
```


