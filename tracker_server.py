# Emma Niemenmaa
# Created: 3.4.2024
# Last modified: 3.4.2024
# Sources:
# 1. Chat app video: https://www.youtube.com/watch?v=3UOyky9sEQY
# 2. Python socket video: https://www.youtube.com/watch?v=YwWfKitB8aA

import threading
import socket
from pysondb import db

# Create data strucktures for handling clients and connections
connections = {}
fileDB = db.getDb("fileDB.json")

# Define the server
HOST = socket.gethostbyname(socket.gethostname()) # This returns the private ip address of the system it is run on.
PORT = 12345
ALIVE = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen() # Number inside specifies how many unexpected connections are allowed before they start getting rejected (Example (5) -> if more than 5 connections are waiting, new requests are denied)
print("Server is listening...")
print(f"Port: {PORT}")
print(f"IP: {HOST}")

def clientDisconnect(owner):
    fileList = fileDB.getByQuery({"owner":owner})
    for file in fileList:
        id = file["id"]
        fileDB.deleteById(id)
    return None

def sendFileList(client):
    fileList = fileDB.getAll()
    for file in fileList:
        message = "FILELIST:" + file["hash"] + ":" + file["fileName"]
        # print("sendFileList:", message)
        client.send(message.encode("utf-8"))
    return None


def handle(client, nickname): # handles the connection
    while True:
        try:
            message = client.recv(1024).decode("utf-8").split(":") # message in the form: ["request", filehash]
            if message[0] == "DOWNLOADREQUEST":
                fileHash = message[2]
                fileDownloader = message[1]
                fileDownloaderIP, fileDownloaderPort = connections[fileDownloader][1]

                fileDict = fileDB.getByQuery({"hash": fileHash})
                fileUploader = fileDict[0]["owner"]

                fileRequestMessage = "FILESENDREQUEST:" + fileHash + ":" + fileDownloaderIP + ":" + str(fileDownloaderPort)
                connections[fileUploader][0].send(fileRequestMessage.encode("utf-8"))


            elif message[0] == "UPLOADREQUEST":
                hashList = fileDB.getByQuery({"hash":message[3]})
                if hashList == []:
                    fileDB.add({
                        "hash": message[3],
                        "owner": message[1],
                        "fileName": message[2]
                    })
                    client.send("UPLOAD:Successful".encode("utf-8"))
                else:
                    client.send("UPLOAD:Failed".encode("utf-8"))

            elif message[0] == "FILELISTREQUEST":
                sendFileList(client)
            
            elif  message[0] == "DISCONNECT":
                del connections[nickname]
                clientDisconnect(nickname)
                print("4:", connections)

        except Exception as e:
            print("(handle) Exception occurred:", e)
            clientDisconnect(nickname)
            del connections[nickname]
            print("3:", connections)
            break

def server_main(connections):
    while True:
        try:
            client, address = server.accept() # Communication socket, lets us communicate with the client
            print(f"Connected with {str(address)}")

            nickname = client.recv(1024).decode("utf-8")

            # A dictionary where UNIQUE nicknames for users is the key and value is a list of their files
            connections[nickname] = [client, address]

            print("Nickname of the client is", nickname + "!")
            # Joskus ku muistetaa ni tehhää databaseluku tai jtn

            thread = threading.Thread(target=handle, args=(client, nickname,))
            thread.start() # This starts the worker (handle) function in a separate thread.

        except ConnectionAbortedError as e:
            print(f"(main) Exception occurred: {e}")
            clientDisconnect(nickname)
            del connections[nickname]
            print("1:", connections)
            continue
        except Exception as e:
            print(f"(main) Exception occurred: {e}")
            clientDisconnect(nickname)
            del connections[nickname]
            print("2:", connections)
            continue

server_main(connections)

print("Server is going offline.")