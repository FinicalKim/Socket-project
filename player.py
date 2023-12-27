import socket

# Set up the socket connection with the server
manager_ip = "127.0.0.1"
IP = ""; portM = 0; portR = 0 ;portP = 0
registered = False

client_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
logicalNetwork_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # list of commands
register = "register <player> <IPv4-address> <m-porti> <r-port> <p-port>"
query_layers = "query-players"
start_game = "start-game <player> <k>"
query_games = "query-games"
end = "end <game-identifier> <player>"
de_register = "de-register <player>"

def retrieve_commands():
    command = input("Enter command: ")
    registerCommand = command
    msg_token = registerCommand.split()
    command2 = msg_token[0]
def setPorts(ip, portm, portr, portp):
    global IP
    global portM
    global portR
    global portP
    IP = ip
    portM = portm
    portR = portr
    portP = portp
    return
def communicate_server():
        # Send the command to the server
    client_socket.sendto(command.encode(), ("localhost", int(portM)))

    # Receive the response from the server
    response, address = client_socket.recvfrom(1024)

    # Decode and print the response
    print(response.decode())
def communicate_logicalRing():
        # Send the command to the logical ring
    client_socket.sendto(command.encode(), (str(IP), int(portR)))

    # Receive the response from the logical ring
    response, address = client_socket.recvfrom(1024)

    # Decode and print the response
    print(response.decode())
def communicate_peer():
            # Send the command to the peers
    client_socket.sendto(command.encode(), (str(IP), int(portP)))

    # Receive the response from the peers
    response, address = client_socket.recvfrom(1024)

    # Decode and print the response
    print(response.decode())

print("List of Commands:\n" + register + "\n" + query_layers + "\n" + start_game + "\n" + query_games + "\n" + end + "\n" + de_register + "\n\n")

while (True):
        # print out a list of commands
    #print("List of Commands:\n" + register + "\n" + query_layers + "\n" + start_game + "\n" + query_games + "\n" + end + "\n" + de_register + "\n\n")

        # Get user input for the command to send to the server
    command = input("Enter command: ")
    registerCommand = command
    msg_token = registerCommand.split()
    command2 = msg_token[0]

    if (command2 == "register"):
        player = msg_token[1]
        IP = msg_token[2]
        portm = int(msg_token[3])
        portr = int(msg_token[4])
        portp = int(msg_token[5])
        setPorts(IP, portm, portr, portp)
    elif (command2 == "de-register"):
        communicate_server()
        exit(1)

    # create the list of commands that interact with the logical ring 
    communicate_server()
