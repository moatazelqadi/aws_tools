"""
This module adds a user specified tag name and value to 'in-use' EBS volumes in a given account.

``Example``
            $python3 add_tag_to_volume.py dummyTagName dummyTagValue

© Moataz ElQadi, 2022
"""

import boto3
import sys

def AddTagToVolume(volume,tagName,tagValue):
    try:        
        volume.create_tags(Tags = [{'Key':tagName,'Value':tagValue}])
    except:
        print('error in {}'.format(volume))
        
def main(tagName,tagValue):
    ec2 = boto3.Session().resource('ec2')
    volumes = list(ec2.volumes.all())
    for v in volumes:
        if v.state == 'in-use':
           print('Adding tag {}={} to {}'.format(tagName,tagValue,v.id))
           AddTagToVolume(v,tagName,tagValue)           
        else:
            print(v.state)

if __name__ == "__main__":   
    try:
        tagName,tagValue = sys.argv[1:]
    except:
        print('Input argument error')
    main(tagName,tagValue)