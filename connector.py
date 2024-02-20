from pprint import pprint
import yaml
import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
    Netmiko
)
result = {}
def send_show_command(device, commands):

    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


if __name__ == "__main__":
        
        txt = input("Type network device: ")
        username = "davsuar"
        password = getpass.getpass('Please enter the password: ')
        device = {
        "device_type": "cisco_ios",
        "host": f"{txt}",         
        "username":  f"{username}",
        "password":  f"{password}",
        "secret":  f"{password}",
        }
    
        with open('commandsCM.txt') as switches:
            for IP in switches:
                Switch = send_show_command(device, [IP] )               
                
        pprint(Switch, width=100)
    
        with open("result.txt", 'w') as f: 
            for key, value in Switch.items(): 
                f.write('\n%s %s\n' % (key, value))
  
        