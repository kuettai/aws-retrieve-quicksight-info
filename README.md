# aws-retrieve-quicksight-info

Go to cloudshell, run the following installing scripts
```
python3 -m venv .
source bin/activate
python3 -m pip install --upgrade pip
git clone https://github.com/kuettai/aws-retrieve-quicksight-info.git
cd aws-retrieve-quicksight-info
pip install boto3
pip install numpy
```

Setup your AWS information
```
export AWS_ACCOUNT_ID="$(aws sts get-caller-identity | jq -r '.Account')"   
export AWS_REGION=ap-southeast-1    # change this to your region
```

```
python3 main.py
```

Download the files using this path: ~/aws-retrieve-quicksight-info/qsinfo.csv
You can find the download button at top right -> ACTIONS -> Downloads file
