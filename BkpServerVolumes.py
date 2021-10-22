"""
This module creates a full image of an EC2 instance by creating a snapshot of each volume attached to the machine.
It takes 2 arguments, CRQ (The change request number) and the instance name.
``Example``
            $BkpServerVolumes.py CRQ1234 ServerName

``ToDo``
            Support multiple servers in one call
"""
import boto3
import datetime
import sys
def main(crq,instanceName):
    #define ISO date string to be used in snapshot name
    yearFromNow = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y%m%d')
    #ec2 high level api
    ec2 = boto3.resource('ec2')
    #find instance by name
    instanceList = ec2.instances.filter(Filters=[{'Name': 'tag:Name','Values': [instanceName]}])
    instance = list(instanceList)[0]    
    #snapshot each volume
    for volume in instance.volumes.all():
        snapshotDesc = '{} {} {}'.format(instanceName,volume.id, crq)
        snapshotName = 'DoNotDeleteBefore{}-{}'.format(yearFromNow,volume.id)
        volume.create_snapshot(Description=snapshotDesc,TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': snapshotName
                    },
                ]
            },
        ])
        
if __name__=="__main__":
    if sys.argv>=3:
        crq = sys.argv[1]
        instanceName = sys.argv[2]
        main(crq,instanceName)
