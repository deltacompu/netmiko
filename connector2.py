from netmiko import ConnectHandler
import getpass
import json
passwd = getpass.getpass('Please enter the password: ')
command = input("Type command: ")

my_devices = list()
with open('devices.txt') as devices:
            for hostanames in devices:
                my_devices.append(hostanames) 

#my_devices = ['air5-fc-agg-t1-a-1', 'air5-fc-agg-t1-a-2', 'air5-fc-agg-t1-a-3', 'air5-fc-agg-t1-a-4'] #list of devices
#my_devices = ['air5-fc-dis-r-4-1.amazon.com', 'air5-fc-acc-sw-4-1', 'air5-fc-acc-sw-4-2', 'air5-fc-acc-sw-4-3', 'air5-fc-acc-sw-4-4', 'air5-fc-acc-sw-4-5', 'air5-fc-acc-sw-4-6', 'air5-fc-acc-sw-4-7', 'air5-fc-acc-sw-4-8', 'air5-fc-acc-sw-4-9'] #list of devices
device_list = list() #create an empty list to use it later
output_list = list()
for device_ip in my_devices:
    device = {
        "device_type": "cisco_ios",
        "host": device_ip,
        "username": "davsuar",
        "password": passwd, # Log in password from getpass
        "secret": passwd # Enable password from getpass
    }
    device_list.append(device)

#json_formatted = json.dumps(device_list, indent=4)
#print(json_formatted)



for each_device in device_list:
    connection = ConnectHandler(**each_device)
    connection.enable()
    print(f'Connecting to {each_device["host"]}')
    output = connection.send_command_timing(f"{command}")
    print(output)
    output_list.append(each_device["host"])
    output_list.append("-------------------")
    output_list.append(output)
    print(f'Closing Connection on {each_device["host"]}')
    connection.disconnect()

with open("result.txt", 'w') as fp: 
    for item in output_list:        
        fp.write("%s\n" % item)
    print('Result saved in a text file')