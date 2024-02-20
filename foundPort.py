from pprint import pprint
import yaml
import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
    Netmiko
    )

access_switch_number=1
def send_show_command(hostname, command):
    device = {
                    "device_type": "cisco_ios",
                    "host": f"{hostname}",         
                    "username":  f"{username}",
                    "password":  f"{password}",
                    "secret":  f"{password}",
                }    
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()            
            output = ssh.send_command(command,use_textfsm=True)
            return output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

if __name__ == "__main__":
        txt = "air5-fc-dis-r-"
        txt2 = "air5-fc-acc-sw-"
        username = "davsuar"
        password = getpass.getpass('Please enter the password: ')
        mac_address = input("Type Mac-Address in Cisco format: ")
        for num in range(1, 10):
            distribution_switch = txt+str(num)+"-1"
            print(distribution_switch)            
            command ="show mac address-table | include "+mac_address 
            result = send_show_command(distribution_switch, command)           
            if (len(result)>0):
                access_switch_number = result[len(result)-1]   
                access_switch = txt2+str(num)+"-"+str(access_switch_number)                
                result = send_show_command(access_switch, command) 
                if (len(result)>0): 
                    print ("Mac Address encountered at "+access_switch+ " port"+result[-8:])                    
                    command_ip="show ip arp | include "+mac_address 
                    show_ip_arp = send_show_command(distribution_switch, command_ip)
                    for item in show_ip_arp:
                        ip = item["address"]
                        vlan = item["interface"]                       
                    print ("IP Address "+ip) 
                    print ("VLAN "+vlan) 
                    break
            
        
  
        