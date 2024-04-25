# DS Final project
# Created: 20.4.2024
# Last modified: 24.4.2024
# Sources:
# 1. Sending and receiving file chunks: https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
# 2. 


'''
1. broadcast: Takes a message as a parameter and sends it to all clients
2. clientDisconnect: Takes the nickname of the client as a parameter and removes their files from the file database (fileDB)
3. sendFileList: Takes the client socket as a parameter and and sends the filelist to a client requesting it.
4. handle: Takes client nickname and sokcket as parameters. Handles message exchange between two clients or client and server.
5. server_main: Takes no parameters. Handles the new clients and connections.
'''

import threading
import socket
from pysondb import db
import os
import time

# Create data strucktures for handling clients and connections
download_queue = {} # In the form: fileHash: downloaderNickname
connections = {} # In the form: nickname: clientSocket

# Recreate the database when server restarts
os.remove("fileDB.json")
fileDB = db.getDb("fileDB.json")

# Define and start the server
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345
ALIVE = False
FILESIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(10) # Number inside specifies how many unexpected connections are allowed before they start getting rejected (Example (5) -> if more than 5 connections are waiting, new requests are denied)
print(f"Server is listening on port {PORT}...")
# print(f"IP: {HOST}")

# Sends a message to all clients
def broadcast(message):
    for nickname in connections:
        connections[nickname].send(message.encode("utf-8"))

# Removes disconnected peer's files from the database
def clientDisconnect(nickname):
    del connections[nickname]
    print("Client removed:", connections)
    fileList = fileDB.getByQuery({"owner":nickname})
    for file in fileList:
        id = file["id"]
        fileDB.deleteById(id)
    return None

# Sends the file list to a client requesting it.
def sendFileList(client):
        try:
            message = "FILELIST"
            fileList = fileDB.getAll() 
            for file in fileList:
                message = message + ":"+ file["hash"] + "-" + file["fileName"]
            client.send(message.encode("utf-8"))
        except Exception as e:
            print("\nsendFileList")
            print("Exception occurred:", e)

# Handles message exchange between two clients or client and server.
def handle(client, nickname):
    while True:
        try:
            # message is a str received from the client. 
            # The message is written in the form: "REQUEST:FileHash:FileName" for example
            message = client.recv(1024).decode("utf-8").split(":")
            option = message[0]

            # Inform uploader for upcoming download request.
            if option == "DOWNLOADREQUEST":
                # Parsing the info from message
                fileHash = message[1]
                
                # Getting the uploader information from the database and the connections list:
                fileDict = fileDB.getByQuery({"hash": fileHash})
                fileUploader = fileDict[0]["owner"]
                 
                # Add the client requesting the file to the download_queue dictionary.
                download_queue[fileHash] = nickname

                # Sends a message to the client who has the file to let them know to start sending it.
                fileRequestMessage = "FILESENDREQUEST:" + fileHash
                connections[fileUploader].send(fileRequestMessage.encode("utf-8"))
                

            # Starts sending the file 
            elif option == "FILE":
                chunkList = []
                fileHash = message[1]
                #fileExtension = fileDB.getByQuery({"hash":fileHash})[0]["fileName"].split(".")[1]
                #tempFile = "temp." + fileExtension

                # Finds the downloaders socket from a downloader_queue dictionary
                if fileHash in download_queue.keys():
                    # Define neccessary variables
                    username = download_queue[fileHash] # Downloaders username
                    downloaderSocket = connections[username]
                    uploaderSocket = client

                    # Start receiving packets from the uploader
                    file_message = uploaderSocket.recv(1024)
                    while file_message:
                        chunkList.append(file_message)
                        file_message = uploaderSocket.recv(1024)
                    
                    # Sending the file to the client who is requesting it
                    message = "FILE:" + fileHash
                    downloaderSocket.send(message.encode("utf-8"))
                    for chunk in chunkList:
                        downloaderSocket.send(chunk)
                    downloaderSocket.shutdown(socket.SHUT_WR)
                    #downloaderSocket.close()
                print(f"Sending file complete. {len(chunkList)} packets sent.")

            # Client wants the server to know that they have a file that they can send to other clients upon request.
            elif option == "UPLOADREQUEST":
                hashList = fileDB.getByQuery({"hash":message[3]})
                
                # If hash is not found on the database already, adds the file info to the database
                if hashList == []:
                    print("Adding file to db")
                    fileDB.add({
                        "hash": message[3],
                        "owner": message[1],
                        "fileName": message[2]
                    })
                else:
                    for data in hashList:
                        if data["owner"] != nickname:
                            print("Adding file to db")
                            fileDB.add({
                                "hash": message[3],
                                "owner": message[1],
                                "fileName": message[2]
                            })
                            # A message to client informing about a successful upload
                            client.send("UPLOAD:Successful".encode("utf-8"))
                        # If the hash can already be found on the database, it won't be added there another time.
                        else:
                            client.send("UPLOAD:Failed".encode("utf-8"))
                
                # Broadcast to every client to tell them to request an updated file list
                updateMessage = "NEWFILE"
                broadcast(updateMessage)
            
            # Sends the contents of fileDB to a client requesting it
            elif option == "FILELISTREQUEST":
                sendFileList(client)
            
            # Removes the client's files from the database when a client disconnects from the network.
            elif  option == "DISCONNECT":
                print(f"Client {nickname} disconnecting")
                clientDisconnect(nickname)
                break

        except ConnectionAbortedError as e:
            print("\nhandle")
            print(f"ConnectionAbortedError, disconnecting {nickname}")
            clientDisconnect(nickname)
            break
        except Exception as e:
            print("\nhandle")
            print("Exception occurred:", e)
            clientDisconnect(nickname)
            break

# Handles the new clients and connections.
def server_main():
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")
            nickname = None
            
            # Checks if users username is unique
            invalid = True
            while invalid:
                nickname = client.recv(1024).decode("utf-8")
                if nickname != None:
                    if nickname in connections.keys():
                        client.send("INVALID".encode())
                    else:
                        client.send("VALID".encode())
                        invalid = False
        

            # A dictionary where UNIQUE nicknames for users is the key and value is a list of their files
            connections[nickname] = client

            print("Nickname of the client is", nickname + "!")

            thread = threading.Thread(target=handle, args=(client, nickname,))
            thread.start() # This starts the worker (handle) function in a separate thread.

        except ConnectionAbortedError as e:
            print("\nmain")
            print(f"ConnectionAbortedError: {e}")
            clientDisconnect(nickname)
            # print("1:", connections)
            continue
        except Exception as e:
            print("\nmain")
            print(f"Exception occurred: {e}")
            clientDisconnect(nickname)
            # print("2:", connections)
            continue

if __name__ == "__main__":
    server_main()

print("Server is going offline.")