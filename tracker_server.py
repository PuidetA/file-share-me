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
download_queue = {} # In the form: hash: downloaderSocket
connections = {}
fileDB = db.getDb("fileDB.json")

# Define and start the server
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345
ALIVE = False
FILESIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(10) # Number inside specifies how many unexpected connections are allowed before they start getting rejected (Example (5) -> if more than 5 connections are waiting, new requests are denied)
print("Server is listening...")
# print(f"Port: {PORT}")
# print(f"IP: {HOST}")

def broadcast():
    message = "NEWFILE"
    for nickname in connections:
        connections[nickname][0].send(message.encode("utf-8"))

# Removes disconnected peer's files from the database
def clientDisconnect(nickname):
    del connections[nickname]
    fileList = fileDB.getByQuery({"owner":nickname})
    for file in fileList:
        id = file["id"]
        fileDB.deleteById(id)
    return None

# 
def sendFileList(client):
        try:
            fileList = fileDB.getAll()
            for file in fileList:
                message = "FILELIST:" + file["hash"] + ":" + file["fileName"]
                client.send(message.encode("utf-8"))
        except Exception as e:
            print("\nsendFileList")
            print("Exception occurred:", e)


def handle(client, nickname): # handles the clients and connections
    while True:
        try:
            message = client.recv(1024).decode("utf-8").split(":") # message in the form: "REQUEST:FileHash:FileName" for example
            # print(message)
            if message[0] == "DOWNLOADREQUEST": # Inform uploader for upcoming download request
                fileHash = message[2]
                
                # Getting the uploader information from the database and the connections list:
                fileDict = fileDB.getByQuery({"hash": fileHash})
                fileUploader = fileDict[0]["owner"]

                download_queue[fileHash] = nickname

                fileRequestMessage = "FILESENDREQUEST:" + fileHash
                connections[fileUploader][0].send(fileRequestMessage.encode("utf-8"))
                

                
            elif message[0] == "FILE":
                chunkList = []
                # counter = 0
                fileHash = message[1]

                # Finds the downloaders socket from a downloader_queue list
                for hash in download_queue:
                    if hash == fileHash:
                        username = download_queue[hash]
                        downloaderSocket = connections[username][0]
                        print(downloaderSocket)

                        file_message = client.recv(1024)
                        while True:
                            if file_message[0].decode() == "CHUNK":
                                file_message = client.recv(1024)
                                if file_message[-5:] == b"<END>":
                                    chunkList.append(file_message[-5:])
                                    break
                                chunkList.append(file_message)
                        
                        print("Pituus: ", len(chunkList))

                        downloaderSocket.send("FILE".encode("utf-8"))
                        for chunk in chunkList:
                            found = chunk.find("FILE".encode())
                            #if found:
                            #    print(chunk)
                            #downloaderSocket.send(file_message)


            elif message[0] == "UPLOADREQUEST":
                print("upload request")
                hashList = fileDB.getByQuery({"hash":message[3]})
                if hashList == []:
                    fileDB.add({
                        "hash": message[3],
                        "owner": message[1],
                        "fileName": message[2]
                    })
                    client.send("UPLOAD:Successful".encode("utf-8"))
                    broadcast()
                else:
                    client.send("UPLOAD:Failed".encode("utf-8"))
                print("upload requestn't")
            
            elif message[0] == "FILELISTREQUEST":
                sendFileList(client)
            
            elif  message[0] == "DISCONNECT":
                clientDisconnect(nickname)
                # print("4:", connections)

        except Exception as e:
            print("\nhandle")
            print("Exception occurred:", e)
            clientDisconnect(nickname)
            # print("3:", connections)
            break

def server_main():
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            nickname = client.recv(1024).decode("utf-8")

            # A dictionary where UNIQUE nicknames for users is the key and value is a list of their files
            connections[nickname] = [client, address]

            print("Nickname of the client is", nickname + "!")

            #thread_filelist = threading.Thread(target=sendFileList, args=(client,))
            #thread_filelist.start()

            thread = threading.Thread(target=handle, args=(client, nickname,))
            thread.start() # This starts the worker (handle) function in a separate thread.

        except ConnectionAbortedError as e:
            print("\nmain")
            print(f"Exception occurred: {e}")
            clientDisconnect(nickname)
            # print("1:", connections)
            continue
        except Exception as e:
            print("\nmain")
            print(f"Exception occurred: {e}")
            clientDisconnect(nickname)
            # print("2:", connections)
            continue

server_main()

print("Server is going offline.")