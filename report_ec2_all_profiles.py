"""
This tool generates a csv report of EC2 instances in all available profiles. 
The report contains the following columns: id, name, state

``Example``
            $python3 report_ec2_all_profiles.py

© Moataz ElQadi, 2022
"""   
import boto3
def instanceToString(i):
	try:
		name =  [tag['Value'] for tag in i.tags if tag['Key']=='Name'][0]
		if name is None:
			name=""
	except:
		name=""
	state=i.state['Name']
	return i.id+','+name+','+state
    
profiles = boto3.session.Session().available_profiles
readOnlyProfiles = [prof for prof in profiles if 'readonly' in prof]
result = ['profile,instance_id,instance_name,state\n']
for profile in readOnlyProfiles:
    try:
        print(profile)
        session = boto3.Session(profile_name=profile)
        ec2 = session.resource('ec2')
        records = [ profile+','+instanceToString(i)+'\n' for i in ec2.instances.all()]
        result.extend(records)
    

    except:
        print("-------error in {}".format(profile))
    
    with open('All_EC2.csv','w') as f:
        f.writelines(result)
    
	