"""
This tool generates a csv report of lambda functions in all available profiles. 
The report contains the following columns profile,function_name,runtime

``Example``
            $python3 report_lambda_all_profiles.py
"""
import boto3
#get all available profiles    
profiles = boto3.session.Session().available_profiles
#select the readonly profiles
readOnlyProfiles = [prof for prof in profiles if 'administrator' in prof]
#create the first line in the result csv, containing the header
result = ['profile,function_name,runtime\n']

for profile in readOnlyProfiles:
    try:
        print(profile)
        #get a session for the profile
        session = boto3.Session(profile_name=profile)
        #get a low-level client for lambda api
        lam = session.client('lambda')
        #call list_functions (which returns only 50 results/page)
        pages = lam.get_paginator('list_functions').paginate()
        #get a list of pages, each page contains a list of functions
        pages = list(pages)
        #fns is a "flat list" of all functions in all pages in the profile
        fns=[]
        for page in pages:
            fns.extend(page['Functions'])
        #create the csv lines corresponding     
        profile_records = ["{},{},{}\n".format(profile,fn['FunctionName'],fn['Runtime'])   for fn in fns]        
        result.extend(profile_records)
        
    except:
        print("-------error in {}".format(profile))
    #write to file
with open('lambda_all_profiles.csv','w') as f:
    f.writelines(result)
    
	