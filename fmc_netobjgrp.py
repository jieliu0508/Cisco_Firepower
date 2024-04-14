import requests
import json
import re
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning



address = "192.168.2.67"
username = "apiuser"
password = "Postman123!"

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

api_token_uri = "/api/fmc_platform/v1/auth/generatetoken"
url = "https://" + address + api_token_uri

response = requests.request("POST", url, verify=False, auth=HTTPBasicAuth(username, password))

accesstoken = response.headers["X-auth-access-token"]
refreshtoken = response.headers["X-auth-refresh-token"]
DOMAIN_UUID = response.headers["DOMAIN_UUID"]

host_url = "https://" + address + "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/networkgroups"
headers = { 'Content-Type': 'application/json', 'x-auth-access-token': accesstoken }

response = requests.get(host_url, headers=headers, verify=False)

group_name = input("What is the Network Object Group Name? ")

ll = response.json()["items"]
for links in ll:
    for key, val in links.items():
        if val == group_name:
           netgroupid=links["id"]
                  
group_url = "https://" + address + "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/networkgroups/" + netgroupid

attacker_group = requests.get(group_url, headers=headers, verify=False)

ff = json.dumps(attacker_group.json(),indent=4)

#Manually input attacher's IP
#attacker_ip = input("Network Object Group name is AC-Attackers, please enter attacker's IP to add: ")
#if not re.match(r'[0-9]+(?:\.[0-9]+){3}', attacker_ip):
#    print('Invalid IP Address')
#    attacker_ip = input("Network Object Group name is AC-Attackers, please enter attacker's IP to add: ")  

ip_file = input ("please specify text file path and name: ")

f = open(ip_file)
for x in f:
    attacker_ip = x.strip()
    attacker = {"literals":[{"type":"Host","value":attacker_ip}],"type":"NetworkGroup","id":netgroupid}
    add_group_member_url = "https://" + address + "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/networkgroups/" + netgroupid + "?action=add"
    response = requests.put(add_group_member_url, data=json.dumps(attacker), headers=headers, verify=False)
    if response.status_code == 200:
	    print(attacker_ip + " is successfully added to Group " + group_name)
    else:
   	    print("Failed to add " + attacker_ip + " to Group "+ group_name)
        
	

