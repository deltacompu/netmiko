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
result = []
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
        ip_address = input("Type ip-Address: ")       
        for num in range(1, 10):
            distribution_switch = txt+str(num)+"-1"            
            command ="show arp | include "+ip_address 
            show_arp = send_show_command(distribution_switch, command)
            if (len(show_arp)>0):
                result_arp=show_arp.split(' ')
                mac_address = result_arp[16]
                print ("Mac-Address is "+mac_address)
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
                            vlan = item["interface"]  
                        print ("VLAN "+vlan) 
                        break
                 
                       
           