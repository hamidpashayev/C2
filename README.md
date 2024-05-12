# C2 - Command & Control 

This is a Command & Control (C2) project in Python for remote control of client machines.

## Features
- **Encryption**: Communication with clients is encrypted using AES encryption.
- **Command Execution**: Send commands to clients for execution on their machines.
- **File Transfer**: Transfer files between the server and clients.
- **Screenshot Capture**: Capture screenshots from client machines.
- **Client Management**: Manage clients, including renaming, removing, and listing active clients.
- **Location Tracking**: Retrieve the geographical location of clients based on their IP addresses.

## Installation
1. Clone the repository:
`git clone https://github.com/hamidpashayev/C2.git`

2. Navigate to the project directory: `cd C2`

3. Install the required Python packages using pip:
`pip install -r requirements.txt`


## Usage
1. Start the C2 server by running the script.
   `python3 ./server.py`
3. Connect clients to the server by running the client script on target machines.
4. Use the server to send commands, transfer files, capture screenshots, and manage clients.

## Commands
- `active`: List all active clients.
- `rename <old_client_name> <new_client_name>`: Rename a client.
- `select <client_name>`: Select a client for sending commands.
- `e`: Output information about a client and write to `enumeration.txt`.
- `f <path>`: Get a file from a client.
- `ss`: Get a screenshot from a client.

Note: Active clients list are redirected to `clients.json` file when `exit` command entered on server side.

For more information and help, use the `help` command.

## Getting Help
If you need help with this project, you can:
- Read the documentation in the repository.
- Reach out to us via email at 500pasham@gmail.com.

