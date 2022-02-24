import sys
import boto3
import datetime
import csv
"""
This tool generates a csv report of snapshot ids (snapshots_accountID.csv), creation date, and tags.
It accepts the optional parameter (lastYearToReport)
``Parameters``
            
            lastYearToReport: The year (e.g. 2022) where snapshots are not reported if newer. The default is the current year.

``Example``
            $python3 reportSnapshots.py  2020
"""
def ReportSnapshots(lastYearToReport):
    this_account_id =  boto3.client('sts').get_caller_identity().get('Account')
    ec2 = boto3.Session().resource('ec2')
    snapshots = ec2.snapshots.filter(OwnerIds = [this_account_id])
    with open(r'snapshots_{}.csv'.format(this_account_id),'w') as f:
        writer = csv.writer(f)
        writer.writerow(('id','year','month','day','tags'))
        for s in snapshots:
            if s.start_time.year > lastYearToReport:
                continue
            
            try:
                tagString = str([(tag['Key'],tag['Value']) for tag in s.tags])
            except:
                tagString = ''
            writer.writerow((s.id,s.start_time.year,s.start_time.month,s.start_time.day,tagString))
            
if __name__ == "__main__":   
    lastYearToReport = datetime.datetime.now().year
    try:
        lastYearToReport = int(sys.argv[1])
    except:
        pass
    ReportSnapshots(lastYearToReport)
    