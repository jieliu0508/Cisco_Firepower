from netmiko import ConnectHandler

asa1 = {
    "device_type":"cisco_asa",
    "host":"10.1.2.254",
    "username":"admin",
    "password":"Admin123",
    "secret":"Admin123"
}

ftd1 = {
    "device_type":"cisco_ftd",
    "host":"10.1.2.253",
    "username":"admin",
    "password":"*Jl2002$!"
 }

attacker_ip = "1.1.1.1"
net_connect = ConnectHandler(**ftd1)
print(net_connect.find_prompt())
#output = net_connect.send_command_timing(command_string=f"shun {attacker_ip}",expect_string=r"<")
output = net_connect.send_command_timing(command_string=f"shun {attacker_ip}")


print(output)


# if r">" in output:
#     print("Doing enable")
#     # we need to enable"
#     #net_connect.send_command(command_string="en", expect_string=r"assword:")
#     output=net_connect.send_command(command_string="en")
#     print(output)
#     #print("Got password prompt")
#     #net_connect.send_command(command_string="", expect_string=r"#")

# output = net_connect.find_prompt()
# print(output)
net_connect.disconnect()
