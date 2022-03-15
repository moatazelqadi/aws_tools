# <strong> aws_tools </strong>
Tools for automating common AWS managemnt tasks
## <strong>add_account_id</strong>
### Motivation
In a multi-account AWS organisation, resources from individual accounts can be  backed up and copied to a central repository. In this setup, the cost of retaining backups is attributed to the central account not the account owning the original resource.
### Solution
This tool adds and poulates a tag "account_id" to all ec2 instances in a given account. These user added tags will propagate to snaphshots of these instances. When those snapshots are stored in other accounts (e.g. AWS Backup vault), then these tags can be used to identify the original owner account.

## <strong>bkp_server_volumes</strong>
### Motivation
A common operation task in maintaining production loads in AWS is backing up EC2 instances with all their attached EBS volumes.
### Solution
This module creates a full image of an EC2 instance by creating a snapshot of each volume attached to the machine.
The script accepts 2 arguments, CRQ (The change request number) and the instance name.

## <strong>report_snapshots</strong>
### Motivation
Creating snapshots of EC2 instances can be a good practice. However, over time, those snapshots accumulate over time eating up unnecessary costs. Reporting existing snapshots using the AWS EC2 console can prove challenging when there is a large number of snapshots. 
### Solution
This tool generates a csv report of snapshot ids (snapshots_accountID.csv), creation date, and tags.
It accepts the optional parameter (lastYearToReport) where snapshots are not reported if newer. The default is the current year.

## <strong>delete_snapshots</strong>
### Motivation
Creating snapshots of EC2 instances can be a good practice. However, over time, those snapshots accumulate over time eating up unnecessary costs. Deleting existing snapshots using the AWS EC2 console can prove challenging when there is a large number of snapshots. 
### Solution
This tool removes EBS snapshots given in a csv report created by the report_snapshots tool .
This script expects an input parameter referencing the csv report generated by the report_snapshots tool. The report is in human-readble csv format that can be edited using a spreadsheet or text editor before running the delete_snapshots tool

## <strong> report_lambda_all_profiles </strong>
### Motivation
Lambda serverless compute can be indespensible, thanks to being scalable and versatile. Reporting on all existing lambda functions and their runtimes can prove tricky, especially in big organisations with multiple accounts. Such a report can be valuable where, for example, there is a need to upgrade a runtime, or to define skillsets needed to maintain an account.
### Solution
This tool generates a csv report of lambda functions in all available profiles. 
The report contains the following columns profile,function_name,runtime