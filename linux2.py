from pprint import pprint
import re
import smtplib
from email.mime.text import MIMEText
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
  
    linux = {
        'device_type': 'linux',
        'ip': '10.9.136.43',
        'username': 'rfidadm',
        'password': '',
        'port': 22,
        'verbose':True
        }
    try:
        connection = ConnectHandler(**linux)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        msg = MIMEText("RFID reader is down, if you receive this email is because the RFID reader located at the main door in the main building is down and it needs to be restared")
        msg['Subject'] = "RFID reader is down"
        msg['From'] = 'davsuar@amazon.com'
        msg['To'] = 'davsuar@amazon.com'

        s = smtplib.SMTP('localhost')
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()

    output = connection.send_command('ps -aux | grep RFID')
    test= re.findall('RFID_ReaderV3.jar', output)
    if len(test)>0:
        print(test)
        print("RFID reader is running")
    else:
        print("Service down") 
        linux = {
        'device_type': 'linux',
        'ip': '10.9.136.43',
        'username': 'rfidadm',
        'password': '',
        'port': 22,
        'verbose':True
        }        
        connection = ConnectHandler(**linux)
        output = connection.send_command('nohup java -jar /mnt/data/app/RFID_ReaderV3.jar &')
        
    connection.disconnect()
        