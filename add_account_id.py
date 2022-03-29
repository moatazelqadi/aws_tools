"""
This module adds and poulates a tag "account_id" to all ec2 instances in a given account.
These user added tags will propagate to snaphshots of these instances. When those snapshots are stored in other accounts (e.g. AWS Backup vault), then these tags can be used to identify the original owner account.
``Example``
            $python3 add_account_id.py 

``ToDo``
            Add other resource types
            
© Moataz ElQadi, 2022
"""
import boto3
this_account_id =  boto3.client('sts').get_caller_identity().get('Account')
instances = boto3.Session().resource('ec2').instances.all()
for i in instances:
    print('checking ',i)
    if i.tags is not None:    
        tags =  [ tag for tag in i.tags if tag['Key']=='account_id']
        if tags !=[]:
            tag = tags[0]
            if tag['Value'] ==   this_account_id:
                continue
    i.create_tags(Tags = [{'Key':'account_id','Value':this_account_id}])
    print('Added or created account id %s for instance %s'%(this_account_id,i.id))    
    print()
    
