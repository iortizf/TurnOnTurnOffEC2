import boto3
import datetime

region = 'us-east-1'
ec2client = boto3.client('ec2', region_name = region)
start_date = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

def getInstaceName(tags):
    for tags in tags:
        print("Tag Key=" + tags["Key"] + ",Tag Value="+tags["Value"])
        if tags["Key"] == 'Name':
            return tags["Value"]
    return ''

def startInstances( instances ):
    ec2client.start_instances(InstanceIds=instances)

def stopInstances( instances ):
    ec2client.stop_instances(InstanceIds=instances)
    
def backupInstances( instances ):
    ec2 = boto3.resource('ec2', region_name = region)
    for idInstance in instances:
        instance = ec2.Instance(idInstance)
        if instance is not None:
            instanceName = getInstaceName(instance.tags)
            backupName = idInstance + 'Backup' if instanceName == '' else instanceName +' Backup'
            print("Nombre backup="+backupName)
            ec2client.create_image(Description=backupName, DryRun=False, 
            InstanceId=idInstance, Name=backupName+'-v'+start_date, NoReboot=False)

def lambda_handler(event, context):
    action = event['action']
    instances = event['instances']
    if action == 'stop':
        stopInstances(instances)
    elif action == 'start':
        startInstances(instances)
    elif action == 'backup':
        backupInstances(instances)
