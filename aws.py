# this script is used with region
# us-east-2

import boto3, json, subprocess, re, time
client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

response = client.create_key_pair(
    KeyName='gcp',
    )
#print(response)
with open('gcp.json', 'w') as outfile:
    json.dump(response, outfile)
# grab KeyMaterial to export as .pem
gcpkey = response['KeyMaterial']
# Write to file
file = open("gcp.pem", "w")
file.write(gcpkey)
file.close()
# change file permissions
subprocess.call(['chmod', '0444', 'gcp.pem'])

# create ec2 instance
instance = ec2.create_instances(
    ImageId='ami-0cd3dfa4e37921605',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='gcp')
print(instance)
print("~/pa4/gcp.pem")

#find id and print ip address
matchObj = re.search( r'(i\-\w+)', str(instance), re.M|re.I)

print("Waiting for EC2 instance to boot up. Please wait")
time.sleep(60)
print("Grabbing public IP")
if matchObj:
        instanceId = matchObj.group(1)
        i = ec2.Instance(instanceId)
        publicIp = i.public_ip_address
        print(" ")
        print("Public IP: " + str(publicIp))
