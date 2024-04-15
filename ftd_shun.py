from netmiko import ConnectHandler
from getpass import getpass
import time
import socket


ftd_username = input("Please input FTD CLI Username: ")
ftd_password = getpass()



ftd1 = {
    "device_type":"cisco_ftd",
    "host":"",
    "username":ftd_username,
    "password":ftd_password
 }



SERVER = ""
PORT = 6789

SERVER = socket.gethostbyname(socket.gethostname())



serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((SERVER, PORT))
print(f"\nScript server {SERVER} is listening on UDP port {PORT}......**** Please make sure Windows firewall is allowed the connection ****")


log_num = 0
attacker_ip=""
failures_to_shun = int(input("\nHow many repeated login failures from the same IP need be shunned? please imput a number: "))
print(f"\nOkay, you want to shun repeated {failures_to_shun} login failure, I am listening now ......")
failed_times = 0
attacker_ip_list=[]   # a list store attacker's IP
start=time.time()
    


while True: #run forever
    data, addr = serverSocket.recvfrom(1024)
    #print(addr[0])
    if "113005" in str(data):
        ftd1["ip"]= addr[0]
        print(f'\n{data}')
        log=  str(data)
        cur = time.time()
        if cur-start > 3600 and len(attacker_ip_list) > 0:
            print("Last login failure is one hour again, creating a new attacker IP list!")
            attacker_ip_list.clear() 
        attacker_ip = log[log.find("IP")+5:-3]
        if attacker_ip in attacker_ip_list:      #if the attacker IP is already in the list
            attacker_ip_list.append(attacker_ip)  
            if len(attacker_ip_list) == failures_to_shun:  # reach failure threshold
                print(f"!!!!!! {attacker_ip}  has {failures_to_shun} failed login, requesting FTD {addr[0]} to shun the IP......")
                ssh_conn = ConnectHandler(**ftd1)
                output = ssh_conn.send_command(command_string=f"shun {attacker_ip}",expect_string=r">",read_timeout=20)
                print(output)
                ssh_conn.disconnect() 
                attacker_ip_list.clear()
                start = time.time()
                
            else:
                print(f"FTD {addr[0]} see {len(attacker_ip_list)} login failures from {attacker_ip}." )
                start = time.time()
        
        else:                                     # if it is a new attacker IP, clear the list and add new IP to the list
            print(f"FTD {addr[0]} see a new login failure from {attacker_ip}. " )
            attacker_ip_list.clear()           
            attacker_ip_list.append(attacker_ip) 
            start = time.time()