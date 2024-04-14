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
    "host":"10.10.11.254",
    "username":"admin",
    "password":"*Jl2024$!"
 }

attacker_ip = "1.1.1.1"
net_connect = ConnectHandler(**ftd1)
print(net_connect.find_prompt())  #FXOS prompt <
output = net_connect.send_command_timing(command_string=f"shun {attacker_ip}")
print(output)
# net_connect.send_command_timing(command_string="system support diagnostic-cli")
# prompt = net_connect.find_prompt()

# print(prompt)



# if r">" in prompt:
#     print("Doing enable")
# #     #we need to enable"
# #     #net_connect.send_command(command_string="en", expect_string=r"assword:")
#     net_connect.send_command_timing(command_string="en")
#     print(net_connect.find_prompt())

#     # net_connect.send_command(command_string="", expect_string=r"#")
#     # print(net_connect.find_prompt())
# output = net_connect.send_command_timing(command_string=f"shun {attacker_ip}")
# print(output)
net_connect.disconnect()
