# DS Final project
# By: Emma Niemenmaa, Aino Räkköläinen
# Created: 20.4.2024
# Last modified: 24.4.2024
# Sources:

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
print("Server is listening...")
# print(f"Port: {PORT}")
# print(f"IP: {HOST}")

# Sends a message to all clients
def broadcast(message):
    for nickname in connections:
        connections[nickname].send(message.encode("utf-8"))

# Removes disconnected peer's files from the database
def clientDisconnect(nickname):
    del connections[nickname]
    fileList = fileDB.getByQuery({"owner":nickname})
    for file in fileList:
        id = file["id"]
        fileDB.deleteById(id)
    return None

# Sends the file list to a client requesting it.
def sendFileList(client):
        try:
            fileList = fileDB.getAll()
            for file in fileList:
                message = "FILELIST:" + file["hash"] + ":" + file["fileName"]
                client.send(message.encode("utf-8"))
        except Exception as e:
            print("\nsendFileList")
            print("Exception occurred:", e)

# Handles message exchange between two clients or client and server.
def handle(client, nickname):
    while True:
        try:
            # message is a str received from the client. 
            # It is written in the form: "REQUEST:FileHash:FileName" for example
            message = client.recv(1024).decode("utf-8").split(":")

            # Inform uploader for upcoming download request.
            if message[0] == "DOWNLOADREQUEST":
                fileHash = message[2]
                
                # Getting the uploader information from the database and the connections list:
                fileDict = fileDB.getByQuery({"hash": fileHash})
                fileUploader = fileDict[0]["owner"]
                 
                # Add the client requesting the file to the download_queue dictionary.
                download_queue[fileHash] = nickname

                # Sends a message to the client who has the file to let them know to start sending it.
                fileRequestMessage = "FILESENDREQUEST:" + fileHash
                connections[fileUploader].send(fileRequestMessage.encode("utf-8"))
                

            # Starts sending the file 
            elif message[0] == "FILE":
                chunkList = []
                fileHash = message[1]
                fileExtension = fileDB.getByQuery({"hash":fileHash})[0]["fileName"].split(".")[1]
                tempFile = "temp." + fileExtension

                # Finds the downloaders socket from a downloader_queue dictionary
                if fileHash in download_queue.keys():
                    username = download_queue[fileHash]
                    downloaderSocket = connections[username]
                    uploaderSocket = client
                    #print("downloaderSocket:", downloaderSocket)
                    #print("Nickname:", username)
                    #print("uploaderSocket:", client)
                    #print("Nickname:", nickname)
                    file_message = client.recv(1024)
                    while file_message:
                        chunkList.append(file_message)
                        file_message = client.recv(1024)
                        
                    print(f"File received. {len(chunkList)} packets sent.")
                    
                    message = "FILE:" + fileHash
                    downloaderSocket.send(message.encode("utf-8"))

                    # Writes the received chunks into a temporary file
                    file = open(tempFile, "wb")
                    for chunk in chunkList:
                        file.write(chunk)
                    file.close()
                    # file_size = os.path.getsize(tempFile)
                    # print("File Size is :", file_size, "bytes")
                    # Sends the tempFile to the client requesting the file
                    file = open(tempFile, "rb")
                    chunk = file.read(FILESIZE) 
                    counter = 0
                    while chunk:
                        counter += 1
                        # print(chunk)
                        downloaderSocket.send(chunk)
                        chunk = file.read(FILESIZE)
                    # downloaderSocket.send(chunkList[len(chunkList)-1])
                    file.close()
                    #for chunk in chunkList:
                    #    downloaderSocket.send(chunk)
                    time.sleep(0.5)
                    downloaderSocket.shutdown(socket.SHUT_WR)
                    os.remove(tempFile)
                print(f"Sending file complete. {counter} packets sent.")


            # Client wants the server to know that they have a file that they can send to other clients upon request.
            elif message[0] == "UPLOADREQUEST":
                print("upload request")
                hashList = fileDB.getByQuery({"hash":message[3]})
                # If hash is not found on the database already, adds the file info to the database
                if hashList == []:
                    fileDB.add({
                        "hash": message[3],
                        "owner": message[1],
                        "fileName": message[2]
                    })
                    # A message to client informing about a successful upload
                    client.send("UPLOAD:Successful".encode("utf-8"))
                    message = "NEWFILE"
                    # Broadcast to every client to tell them to request an updated file list
                    broadcast(message)
                # If the hash can already be found on the database, it won't be added there another time.
                else:
                    client.send("UPLOAD:Failed".encode("utf-8"))
                print("upload requestn't")
            
            # Sends the contents of fileDB to a client requesting it
            elif message[0] == "FILELISTREQUEST":
                sendFileList(client)
            
            # Removes the client's files from the database when a client disconnects from the network.
            elif  message[0] == "DISCONNECT":
                clientDisconnect(nickname)
                break

        except Exception as e:
            print("\nhandle")
            print("Exception occurred:", e)
            clientDisconnect(nickname)
            # print("3:", connections)
            break


# Handles the new clients and connections.
def server_main():
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            nickname = client.recv(1024).decode("utf-8")

            # A dictionary where UNIQUE nicknames for users is the key and value is a list of their files
            connections[nickname] = client

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

if __name__ == "__main__":
    server_main()

print("Server is going offline.")