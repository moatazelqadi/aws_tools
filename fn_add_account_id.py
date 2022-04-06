"""
This module adds and poulates a tag "account_id" to all ec2 instances, volumes, and snapshots in a given account.
These user added tags will propagate to snaphshots of these instances. When those snapshots are stored in other accounts (e.g. AWS Backup vault), then these tags can be used to identify the original owner account.
            
© Moataz ElQadi, 2022
"""
import boto3

def addIdToResources(this_account_id,resources):
    for r in resources:
        logger.info('checking ',r)
        if r.tags is not None:    
            tags =  [ tag for tag in r.tags if tag['Key']=='account_id']
            if tags !=[]:
                tag = tags[0]
                if tag['Value'] ==   this_account_id:
                    continue
        r.create_tags(Tags = [{'Key':'account_id','Value':this_account_id}])        
        print('Added or created account id %s to %s'%(this_account_id,r.id))    
        print()
        

def tagInstances(this_account_id):
    print('**Tagging instances**')
    ec2 = boto3.Session().resource('ec2')
    instances = ec2.instances.all()
    addIdToResources(this_account_id,instances)

def tagSnapshots(this_account_id):
    print('**Tagging snapshots**')
    ec2 = boto3.Session().resource('ec2')
    snapshots = ec2.snapshots.filter(OwnerIds = [this_account_id])
    addIdToResources(this_account_id,snapshots)

def tagVolumes(this_account_id):
    print('**Tagging volumes**')
    ec2 = boto3.Session().resource('ec2')
    volumes = ec2.volumes.all()
    addIdToResources(this_account_id,volumes)

def lambda_handler(event, context):       
    this_account_id =  boto3.client('sts').get_caller_identity().get('Account')
    tagInstances(this_account_id)
    tagSnapshots(this_account_id)
    tagVolumes(this_account_id)

