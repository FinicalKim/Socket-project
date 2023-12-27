import socket
import json
import random
from random import shuffle # Import the SHUFFLE function from the RANDOM library.
from random import randint # Import RANDOM INTEGER function.
from random import choice # Import choice. 
from time import sleep # Use the SLEEP function from the TIME library.
import sys # Allows access to OS calls.
import pprint

    # ((5/x) * 1000) + 1000) = 3500, ((5/x) * 1000) + 1499) = 3999
    # Allowed port range is [3500, 3999]

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # read Port-m from stdin
#portM = input("Please enter Port-m (3500-3999): \n")
#while(int(portM) < 3500 and int(portM) > 3999):
port_M = True
while(port_M):
    portM = input("Please enter Port-m (3500-3999): \n")

    if (int(portM) > 3500 and int(portM) < 3999):
        print("Manager port is within range of 3500 and 3999: \n")
        port_M = False


# Bind the socket to a specific IP address and port
sock.bind(('localhost', int(portM)))
print("[Server deployed] The server is listening!\n")

    # Define the playerDatabase for storing player information and the gameDatabase that stores each existing game
    # The keys are player names and the values are tuples of (IP address, port-m, port-r, port-p)
playerDatabase = {} # Stores all the information of the players that are registered 
gameDatabase = {}   # Stores the information of the running games
portR = {}  # Used for the logical network communication
portP = {}  # Used for peer to peer communication
numberOfPlayers = 0
numberOfGames = 0
dealer = {} # stores the inforamtion of the dealers and ther respective game identifiers
numCardsToDeal = 5 #number of cards delt to each player 
onGoingGames = [] #Stores a list for all ongoing game info needed
previousPlayer = ""
totalBooks = 0
address = []
addressIndex = 0

### Go fish code ###

class Player:
    def __init__(self, NAME):
        self.NAME = NAME
        self.HAND = []
        self.score = 0
        self.rightNeighbor = None
        self.leftNeighbor = None
        self.addr = None


# functioning check for books, remove found books, and increase players points
def checkBooks(player):
    global totalBooks
    response = ""
    # print("I'm checking to see if player contains books")
    matches = {}
    for card in player.HAND:
        value = card[0]
        if value in matches:
            matches[value].append(card)
        else:
            matches[value] = [card]

    for value, cards in matches.items():
        if len(cards) == 4:
            player.score += 1
            totalBooks+=1
            print(f"Player {player.NAME} has a set of {value}s!")
            response = (f"Player {player.NAME} has a set of {value}s!")
            player.HAND = [card for card in player.HAND if card not in cards]
            printAllHand()
            # check is all 13 books have been collected
            if totalBooks == 13:
                # call tallie score and decide a winner
                response = declareWinner()
                break
    sortHands()
    return response

def declareWinner():
    # needs more, add all players and their score to the checker and evaluate the highest score.
    highestScore = 0
    winnerName = ""
    for player in selectedPlayersObjects:
        if player.score >= highestScore:
            highestScore = player.score
            winnerName = player.NAME
    # winner = max(playerChecker, key = playerChecker.get)
    print(f"Congratulations! {winnerName} is the winner with {highestScore} books!")
    response = (f"Congratulations! {winnerName} is the winner with {highestScore} books!")
    return response

def printHand(player):
    formattedHand = player.HAND
    response = (str(formattedHand).replace(",", "").replace("'", "").replace("Hearts", "H").replace("Clubs", "C").replace("Spades", "S").replace("Diamonds", "D"))#.replace("', '", ""))

    return response

def printAllHand():
    for player in selectedPlayersObjects:
        formattedHand = player.HAND
        formattedHand = (str(formattedHand).replace(",", "").replace("'", "").replace("Hearts", "H").replace("Clubs", "C").replace("Spades", "S").replace("Diamonds", "D"))#.replace("', '", ""))
        print(f"Player {player.NAME} hand: " + str(formattedHand))
        print(f"{player.NAME} current number of books is:{player.score}")
        print("\n")
    return

def sortHands():
    for player in selectedPlayersObjects:
        player.HAND.sort()
    return

def fish(player1, player2, card): # player1 if the requester and player2 is who is being asked
    global previousPlayer
    for u in range(0, len(player2.HAND)):
        # print(player2.HAND[u][0])
        if player2.HAND[u][0] == card:
            print(f"SUCCESS! {player2.NAME} has {card}")
            response = (f"SUCCESS! {player2.NAME} has {card}\n")
            player1.HAND.append(player2.HAND[u])
            player2.HAND.pop(u)
            # print players new hands possibly?
            break
    else:
        print(f"FAILED! {player2.NAME} does not have {card}")
        response = (f"FAILED! {player2.NAME} does not have {card}\n")
        if (len(deck) != 0):
            player1.HAND.append(deck.pop(0))
    print(f"Next player is {player1.rightNeighbor.NAME} \n")
    response += (f"Next player is {player1.rightNeighbor.NAME} \n")
    previousPlayer = player1.rightNeighbor # assign the next player for the fish command
    if (len(previousPlayer.HAND) == 0 and (len(deck) != 0)): # check the right neighbors hand 
        previousPlayer = player1.leftNeighbor
    printAllHand()
    response += checkBooks(player1)
    return response

def getPlayer(player):
        for locatePlayer in selectedPlayersObjects:
            if locatePlayer.NAME == player:
                currentPlayer = locatePlayer
                return currentPlayer

def make_deck():   # This fucntion will shuffle the new deck. 
    global suits
    global values
    global DECK

    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    DECK = [(value, suit) for suit in suits for value in values]
    shuffle(DECK)
    
    return DECK

#create deck 
deck = make_deck()

def getHand(selectedPlayersObjects):
    global hand
    #global deck
    for player in selectedPlayersObjects:
        for x in range(0, 7):
            player.HAND.append(deck.pop(0))  
        checkBooks(player)
    return

def appendAddr(addr):
    global address
    global addressIndex

    address.append(addr)
    # addressIndex+=1

    return

def assignAddr(player):
    global address
    global addressIndex

    for player in selectedPlayersObjects:
        player.addr = address.pop(0)
        # addressIndex=+1
    return

def sendHands():
    for player in selectedPlayersObjects:
        addr = player.addr
        formattedHand = player.HAND
        response = (str(formattedHand).replace(",", "").replace("'", "").replace("Hearts", "H").replace("Clubs", "C").replace("Spades", "S").replace("Diamonds", "D"))#.replace("', '", ""))
        sock.sendto(response.encode(), addr)
    return

# def create_logical_ring(selectedPlayers):
#     playerRing = [] # contains the dealer and k number of players
#     k = len(selectedPlayers) - 1

#     for i, player in enumerate(selectedPlayers):
#         neighbor = selectedPlayers[(i + 1) % (k + 1)]
#         playerObject = selectedPlayers[i]
#         playerObject.rightNeighbor = neighbor  # added code: the players neighbor in the object
# #       playerRing.append((player, playerDatabase[player][2], neighbor, playerDatabase[neighbor][2]))

#     for i, player in enumerate(selectedPlayers):
#         neighbor = selectedPlayers[(i + 1) % (k + 1)]
#         playerObject = selectedPlayers[i]
#         #playerObject.leftNeighbor = neighbor[i-1]  # added code: the players neighbor in the object
# #       playerRing.append((player, playerDatabase[player][2], neighbor, playerDatabase[neighbor][2]))

#     return #playerRing

# def advance_play(playerRing):
#     for i, (player, _, neighbor, neighbor_r_port) in enumerate(playerRing):
#         your_move_command = 'your-move {}'.format(neighbor) # appends the neighbor to variable
#         sock.sendto(your_move_command.encode(), (playerDatabase[player][0], playerDatabase[neighbor][2]))   # sends your move and player data
        
# def shuffle_and_deal_cards(playerRing):


#     for player, r_port, _, _ in playerRing:
#         hand = getHand(player, DECK, numCardsToDeal)
#         currentHand[player] = hand

#     #Send hands to players 
#     for player, hand in currentHand.items():
#         handStr = json.dumps(hand)
#         dealCommand = 'deal {}'.format(handStr)
#         sock.sendto(dealCommand.encode(), (playerDatabase[player][0], r_port))

while (True):
    # Receive a message from a player
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    # Parse the message
    msg_token = message.split()
    command = msg_token[0]
    

    # Process the command       start-game kim 2
    if command == 'register':   # expected input register kim 127.0.0.1 3501 3502 3503    register bre 127.0.0.1 3501 3504 3505     register sadie 127.0.0.1 3501 3506 3507
        # global address
        # global addressIndex

        # address[addressIndex] = addr
        # addressIndex+=1
        appendAddr(addr)

        player = msg_token[1]
        ip_address = msg_token[2]
        portm = int(msg_token[3])
        portr = int(msg_token[4])
        portp = int(msg_token[5])

        if player in playerDatabase:
            response = ("Failed to register player, " + str(player) + " already exist\n")
        else:
            playerDatabase[player] = (ip_address, portm, portr, portp)
            portR[player] = (portr)
            portP[player] = (portp)
            numberOfPlayers += 1
            response = 'SUCCESS. Welcome to Go Fish!\n\n'
            response += ("New player has been added! \nName: " + msg_token[1]+ "\nIPv4: " + msg_token[2] + "\nPort-m: " + msg_token[3] + "\nPort-r: "+ msg_token[4]+ "\nPort-p: " + msg_token[5] + "\n")
            print("New player has been added! \nName: " + msg_token[1]+ "\nIPv4: " + msg_token[2] + "\nPort-m: " + msg_token[3] + "\nPort-r: "+ msg_token[4]+ "\nPort-p: " + msg_token[5] + "\n")
        # Send the response to the player
        sock.sendto(response.encode(), addr)
    
    elif command == 'query-players':
        print("Number of registered players: " + str(numberOfPlayers) + "\n")

        if (numberOfPlayers > 0):
            response = 'SUCCESS. Printing a list of all registered players\n'

            response += ("Number of registered players: " + str(numberOfPlayers) + "\n\n")

            d = playerDatabase
            d = str(d).replace("), ","\n")
            print("Player\t\tIP\tPort-m\tPort-r\tPort-p")
            print(str(d).replace("{","").replace("}", "\n").replace(",", "\t").replace("'", "").replace(":", "\t").replace("},","").replace("(","").replace(")", ""))
            response += ("Player\t\tIP\tPort-m\tPort-r\tPort-p\n")
            d = (str(d).replace("{","").replace("}", "\n").replace(",", "\t").replace("'", "").replace(":", "\t").replace("},","").replace("(","").replace(")", ""))
            response += d
        else:
            response = 'SUCCESS. There are No players registered\n'

        sock.sendto(response.encode(), addr)

    elif command == 'start-game':
        player = msg_token[1]
        k = int(msg_token[2]) 
        global playerRing

        #Check player registration 
        if player not in playerDatabase:
            response = 'Failed, player is not registered'
        #Chack range of k
        elif not 1 <= k <= 4:
            response = 'Failed, k is out of range'
        #Check if at least k players are registered 
        elif len(playerDatabase) < k+1:
            response = 'Failed, not enough players'
        else:
            numberOfGames += 1
            gameIdentifier = numberOfGames #New game identifier

            #Selects at random k other players from those registered in the game
            otherPlayers = list(playerDatabase.keys())
            otherPlayers.remove(player) #removes the dealer 
            selectedPlayers = [player] + random.sample(otherPlayers, k)

            #Create dealer object and add it to database 
            dealerObject = Player(player)
            selectedPlayersObjects = [Player(player) for player in selectedPlayers]

            response = 'SUCCESS. Game {} started!\n'.format(gameIdentifier)
            response += 'Dealer: {} started!\n'.format(player)
            response += 'Participating players: {}\n'.format(", ".join(selectedPlayers))

            # playerRing = create_logical_ring(selectedPlayersObjects) # modified

            k = len(selectedPlayersObjects) - 1

            for i, playerN in enumerate(selectedPlayersObjects):
                neighbor = selectedPlayersObjects[(i + 1) % (k + 1)]
                playerN = selectedPlayersObjects[i]
                # print(f"Iteration {i} for right neighbors: player {playerN.NAME}")
                playerN.rightNeighbor = neighbor  # added code: the players neighbor in the object
                # print(f"Iteration {i} for right neighbors: player {playerN.NAME} and the right neighbor is {playerN.rightNeighbor.NAME}")

            j = 2
            k = 0
            for i, playerN in enumerate(selectedPlayersObjects):
                neighbor = selectedPlayersObjects[j]
                j-=1
                playerN = selectedPlayersObjects[k]
                if k == 0:
                    k = 3
                k-=1
                # print(f"Iteration {i} for right neighbors: player {playerN.NAME}")
                playerN.leftNeighbor = neighbor  # added code: the players neighbor in the object
                # print(f"Iteration {i} for right neighbors: player {playerN.NAME} and the left neighbor is {playerN.leftNeighbor.NAME}")

            assignAddr(selectedPlayersObjects)

            getHand(selectedPlayersObjects)

            dealer[player] = gameIdentifier
            previousPlayer = getPlayer(player) # instantiate the current player for the fish function

            onGoingGames.append((gameIdentifier, player, selectedPlayers))
            printAllHand()
            # sendHands()
        
        print(response)
        sock.sendto(response.encode(), addr)

    elif command == 'query-games':
        print("Number of existing games: " + str(numberOfGames) + "\n"
                + "Number of ongoing games: " + str(len(onGoingGames)) + "\n")
        # display the information on all games
        response = ("\nNumber of existing games: " + str(numberOfGames) + "\n" + "Number of ongoing games: " + str(len(onGoingGames)) + "\n\n")

        if len(onGoingGames) == 0:
            response += "There are no games currently running. \n"
        else: 
            response += "Number of ongoing games: " + str(len(onGoingGames)) + "\n"

            #List of info for each game
            for gameInfo in onGoingGames:
                gameID, dealer, players = gameInfo
                response += "Game ID: {}, Dealer: {}, Players: {}\n".format(gameID, dealer, ", ".join(players))

        #Send response 
        sock.sendto(response.encode(), addr)  

    elif command == 'end':
        player = msg_token[1]
        gID = int(msg_token[2]) 

        #Check if player = dealer and gameID
        if player in dealer and dealer[player] == gID:
            response = 'Success, game {} ended\n'.format(gID)      

            #Remove game from onGoing games list
            onGoingGames = [(gID, dealer, players) for gameID, dealer. players in onGoingGames if gameID != gID]
        else: 
            response = 'FAILURE, invalid game ID or player != dealer\n'
       
        sock.sendto(response.encode(), addr)

    elif command == 'de-register':  # expected input de-register kim
        player = msg_token[1]
        if player not in playerDatabase:
            response = 'Failed to de-register player, player does not exist\n'
        else:
            numberOfPlayers -= 1
            del playerDatabase[player]

            response = (player + ' was de-registered from the game\n')
            print(player + " was de-registered from the game\n")
            # Send the response to the player
        sock.sendto(response.encode(), addr)

    elif command == 'exit':
        if player not in playerDatabase:
            response = 'Closing the server'
        else:
            # Delete the player's account information
            del playerDatabase[player]

            response = 'Closing the server'

        # Send the response to the player
        sock.sendto(response.encode(), addr)
        sock.close()
        False 
        exit(1)
    elif command == 'fish':
        player = msg_token[1]
        card = msg_token[2]
        if card in values:
            targetPlayer = getPlayer(player)
            print(f"{previousPlayer.NAME} is fishing {targetPlayer.NAME} for a {card}!")
            response = fish(previousPlayer, targetPlayer, card)
            #response = 'Fish command executed!'
        else:
            response = 'Invalid card entered'
            print("'Invalid card entered'")

        # Send the response to the player
        sock.sendto(response.encode(), addr)
    elif command == 'h':

        response = printHand(previousPlayer)

        # Send the response to the player
        sock.sendto(response.encode(), addr)

    else:
        response = 'ERROR occured, the command is not found'

        # Send the response to the player
        sock.sendto(response.encode(), addr)
