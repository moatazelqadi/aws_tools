"""
This tool removes EBS snapshots given in a CSV file with "id" column of target snapshots, 
such a report can be created using the report_snapshots tool. 
This script creates a dialog to request input parameters, the change request(CRQ) for the EBS deletion, 
and the input csv file. The CRQ is used as the log file name.

``Example``
            $python3 delete_snapshots.py 

© Moataz ElQadi, 2022
"""

import csv
import logging
import boto3

def deleteSnapshot(ec2,id):
    try:
        collection = ec2.snapshots.filter(SnapshotIds=[id])
        snapshot = list(collection)[0]
        snapshot.delete()
        logging.info('deleted {}'.format(id))
    except:
        logging.error('error with {}'.format(id))

def main(crq,input_file):
    logging.basicConfig(filename='{}.log'.format(crq), level=logging.INFO)
    ec2 = boto3.Session().resource('ec2')
    with open(input_file,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id = row['id']
            deleteSnapshot(ec2,id)

if __name__ == "__main__":   
    sure = input('This program will delete EBS snapshots. Are you sure you want to proceed[Y/N]? ')
    isSure = str.lower(sure) == 'y'
    if isSure:        
        crq = input('What is the CRQ? ')
        input_file = input('Path to CSV file with "id" column of target snapshots: ')
        main(crq,input_file)
    else:
        print('Aborting..')