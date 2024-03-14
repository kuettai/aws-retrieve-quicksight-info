import boto3, botocore, os, json, numpy
from botocore.config import Config

## Input Validation
acctId = os.getenv('AWS_ACCOUNT_ID')
reg = os.getenv('AWS_REGION')

print("Account ID: " + acctId + "; Region: " + reg)

## Setup Environment
dataSetsList = []
rows = [['DataSetId', 'DatasetName', 'DataSetSize(in MB)', 'Sources']]
bConfig = Config(region_name=reg)
qs = boto3.client('quicksight', config=bConfig)

acctInfo = {'AwsAccountId': acctId}

## Script Start
## Acquiring Dataset ID
hasNextToken = True
while(hasNextToken):
    resp = qs.list_data_sets(**acctInfo)
    datasets = resp.get('DataSetSummaries')
    hasNextToken = resp.get('NextToken')
    print(hasNextToken)
    
    for dataset in datasets:
        if dataset['ImportMode'] == 'SPICE':
            obj = {'DataSetId': dataset['DataSetId'], 'Name': dataset['Name']}
            dataSetsList.append(obj)

## Get DataSets spices info
if not dataSetsList:
    print('No dataset found in this region: ' + reg)
    exit()
    
print("There are total of {} dataset(s) that uses SPICE".format(len(dataSetsList)))
    
for ds in dataSetsList:
    print("Processing dataset: " + ds['Name'])
    
    try:
        resp = qs.describe_data_set(
            AwsAccountId=acctId,
            DataSetId=ds['DataSetId']
        )
    
        info = resp.get('DataSet')
        
        # PhysicalTableMap
        # ConsumedSpiceCapacityInBytes
        # row = [ds['Name'], info['ConsumedSpiceCapacityInBytes']/1024/1024, json.dumps(info['PhysicalTableMap'])]
        size = round(info['ConsumedSpiceCapacityInBytes']/1024/1024, 2)
        row = [ds['DataSetId'], ds['Name'], size, json.dumps(info['PhysicalTableMap'])]
        rows.append(row)
        print('Size consumed for this dataset: {} MBytes'.format(size))
        print()
    except botocore.exceptions.ClientError as e:
        print("[NOT SUPPORTED DATASET TYPE] -- " + ds['Name'])
        print(str(e))
        print()
        
if rows:
    outp = numpy.asarray(rows)
    numpy.savetxt("qsinfo.csv", outp, fmt='%s', delimiter="|")