# C2 - Command & Control Server

This is a Command & Control (C2) server implementation in Python for remote control of client machines.

## Features
- **Encryption**: Communication with clients is encrypted using AES encryption.
- **Command Execution**: Send commands to clients for execution on their machines.
- **File Transfer**: Transfer files between the server and clients.
- **Screenshot Capture**: Capture screenshots from client machines.
- **Client Management**: Manage clients, including renaming, removing, and listing active clients.
- **Location Tracking**: Retrieve the geographical location of clients based on their IP addresses.

## Installation
1. Clone the repository:
`git clone https://github.com/your-repo/C2-server.git`

2. Navigate to the project directory:

`cd C2-server`

3. Install the required Python packages using pip:
`pip install -r requirements.txt`


## Usage
1. Start the C2 server by running the script.
2. Connect clients to the server by running the client script on target machines.
3. Use the server to send commands, transfer files, capture screenshots, and manage clients.

## Commands
- `active`: List all active clients.
- `rename <old_client_name> <new_client_name>`: Rename a client.
- `select <client_name>`: Select a client for sending commands.
- `e`: Get information about a client.
- `f <path>`: Get a file from a client.
- `ss`: Get a screenshot from a client.

For more information and help, use the `help` command.

## Getting Help
If you need help with this project, you can:
- Read the documentation in the repository.
- Report issues or ask questions on the [issue tracker](https://github.com/your-repo/C2-server/issues).
- Join our community forums [here](https://your-forum-url.com).
- Reach out to us via email at [your-email@example.com].
- Follow us on social media for updates and announcements.

We're here to help, so don't hesitate to ask if you encounter any problems or have any questions!
