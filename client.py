
"""
DS Final project: Development BRANCH
Created: 20.4.2024
Last modified: 25.4.2024
Client-Side Functionality which can be tested in this branch

Reason for simplified design: The initial design was too complex for the given amount of time. The new design focuses on the core functionalities needed for a basic file-sharing system.
The focus will be more on P2P sharing between only 2 systems. The client will handle file management, peer management, and file exchange.

1. File Handling

calculateFileHash(filePath): Generates a unique hash (like SHA-1) to identify the file on the network.
divideFileIntoChunksAndSendChunks(filePath, chunkSize): splits the file into chunks and sends those for more efficient use

2. File Exchange
requestFile(fileHash): Send a download request to the target server
getFilePath(fileName): Finds the path of file when uploading file with filename given in terminal
uploadFile(): uploads the filehash, filename and file owner information to the target server
sendFileNamesToServer(): used to send names of files user has in files folder which located to the same place than this app
connectToTargetServer(): used to connect to target server with given ip address and port





Sources for this code: 
1) How to use sockets is done based on this video: https://www.youtube.com/watch?v=YwWfKitB8aA
2) Sending and receiving chunks of file with TCP connection in Python is based on this: https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
+ Documentation of Python and each module which were used in this

"""




import hashlib # Can be used for generating hash values.
import os # Can be used for file operations.
import sys
import time
import random
import socket
import threading

fileDict = {}       # Dictionary of files available for sharing. Form: hash value of the file as key and fileName as value
isAlive = True
CHUNK_SIZE = 1024

# 1. File Handling
# This function calculates hash value for each file in the network
def calculateFileHash(filePath):
    """
    Generates a unique hash (like SHA-1) to identify the file on the network.
    Parameters:
    - filePath: The path to the file for which the hash is to be calculated. E.g. "C:/Users/User/Documents/file.txt".
    Returns:
    - hashValue: The calculated hash value for the file. E.g. "a1b2c3d4".
    """
    # Source for this is the documentation of hash module
    with open(filePath, "rb", buffering=0) as file: 
        digest = hashlib.file_digest(file, "sha256")

    hashValue = digest.hexdigest() 
    return hashValue

# This function reads 1 kB chunks from file and sends them to server
def divideFileIntoChunksAndSendChunks(client, filePath, chunkSize):
    """
    Splits the file into smaller chunks for efficient transfer

    Parameters:
    - client: The socket created for this client
    - filePath: The path to the file to be divided into chunks. E.g. "C:/Users/User/Documents/file.txt".
    - chunkSize: The size (in bytes) of each chunk. E.g. 1024 bytes.

    Returns:
    - None """
    try:
        with open(filePath, "rb") as file:
            chunk = 0
            byte = file.read(chunkSize) 
            while byte:
                print("Sending chunk", chunk)
                client.send(byte)
                byte = file.read(1024)
                chunk += 1
            client.shutdown(socket.SHUT_RDWR)
            print("File send to the server")
    except FileNotFoundError:
        print("Check the file name and try again")
    except Exception as e: 
        print(f"Try again, error: {e}")

# This function tries to find the path of file by its name 
def getFilePath(fileName):
    try:
        if(fileName):
            current_directory = os.getcwd() + "\\files"
            path = os.path.join(current_directory, fileName)
            return path
        else: 
            return None
    except FileNotFoundError as e:
        print(f"File not found: {e}")
#   2. User Interface (UI)
def displayFileList():
    """
    Updates the UI with the list of files available for download from other peers. E.g. displays a list of files in a window.

    Parameters: None

    Returns: None
    """

def updateFileList():
    """
    Updates the file list to reflect new files that are added to the folder. i.e. a button that triggers the update and adds it to fileList = [].

    Parameters: None

    Returns: None
    """

def shareFileList(fileList):
    """
    Triggered when displayFileList() method from another peer requests a list of files.

    Parameters:
    - fileList: The list of files available for sharing. E.g. ["file1.txt", "file2.txt"].

    Returns: None
    """

def updateDownloadProgress(fileHash, progress):
    """
    Visually displays download progress of a file (or how many chunks are left to be downloaded).

    Parameters:
    - fileHash: The hash value identifying the file being downloaded. E.g. "a1b2c3d4".
    - progress: The download progress, indicating how many chunks are left to be downloaded. E.g. 5/64 chunks downloaded. In the terminal, it can be displayed as "Downloading file: 5/64".

    Returns: None
    """

# 3. File Exchange/Transfer

# This function sends request to the target server about the file the client wants to download
# The target server checks if any currently connected client has the file
def requestFile(client, fileHash):
    """
    Send a request to the tracker server.
    """
    message = "DOWNLOADREQUEST:" + fileHash
    client.send(message.encode("utf-8"))
    print("File request send")
# This function sends the information about file which is uploaded to the target server which saves
# that information into database that is JSON format.
# Client sends their own username, name of the file and hash value of the file
def uploadFile(client, username, fileName):
    filePath = getFilePath(fileName)
    if (filePath):
        fileHash = calculateFileHash(filePath)
        try:
            request = "UPLOADREQUEST:" + username + ":" + fileName + ":" + fileHash
            client.send(request.encode("utf-8"))
            print("Upload request sent successfully")
        except Exception as error: 
            print(f"Upload request failed, error{error}")
    else:
        print("File path not found!")
# This function is used to send file names to the target server and it takes those files which
# user has added to files folder which should be located in same folder as this app. 
def sendFileNamesToServer(client, username):
    try:
        filesDirPath = os.getcwd() + "\\files"
        fileList = os.listdir(filesDirPath)
        if (len(fileList) > 0):
            for file in fileList:
                uploadFile(client, username, file)
                time.sleep(0.1)
    except Exception as e:
        print(f"Error occured file sending file list: {e}")


# This function tries to connect the client to the tracker server
def connectToTargetServer(client, address, port):
    try:
        client.connect((address, port))
    except Exception as e: 
        print(f"Exception occurred in connecting to the target server: {e}")
# This function listens for server for checking whether their username was unique or not meaning whether their connection succeeded
def listenForNicknameStatus(client):
    username = None
    status = "INVALID"
    print("Welcome to use the program!")
    while True:
        username = input("Give your username: ")
        client.send(username.encode("utf-8"))
        status = client.recv(1024).decode("utf-8")
        if(status == "VALID"):
            sendFileNamesToServer(client, username)
            break
        else:
            print("Invalid username, try again")
    return username
# This function listens for messages that are coming from the server and responds to them
# based on the options it has which are FILELIST, UPLOAD, NEWFILE, FILESENDREQUEST, FILE

def listenForServerConnection(client, serverIP, port):
    """
    Messages server can be received from the target server and what is supposed to happen in client-side:
    FILELIST -- Updates the dictionary (fileDict) containing files that are available for sharing
    UPLOAD -- Tells the status of the uploading file info to the database
    NEWFILE -- Server informs the client to update their fileDict because some other client has uploaded new files to the network
    FILESENDREQUEST -- Client receives this request when some other client asks to download the file through the target server
    -- When this message is received, the client starts to send the requested file to the server in chunks by calling the divideFileIntoChunksAndSendChunks-function
    FILE -- Here the client starts to receive the chunks of file which are stored into temporary list and from there written to the new file which is the received file 
    """

    while True:
        try:
            # Here we receive the message from the tracker server and act according it
            message = client.recv(1024).decode("utf-8").split(":")
            option = message[0]
            if(option == "FILELIST"): # Here we update the list of files
                fileHash = message[1]
                fileName = message[2]
                if (fileHash not in fileDict):
                    fileDict[fileHash] = fileName
            elif(option == "UPLOAD"): # 
                uploadStatus = message[1]
                print("Upload state: " + uploadStatus)
            elif(option == "NEWFILE"):
                print("Updating file list..")
                client.send("FILELISTREQUEST".encode("utf-8"))
            elif(option == "FILESENDREQUEST"):
                print("Received request for sending file to the server")
                fileHash = message[1]
                fileName = None
                print("File dict when sending file:", fileDict)
                if(len(fileDict) > 0):
                    print(fileDict[fileHash])
                    fileName = fileDict[fileHash]
                    if(fileName):
                        filePath = getFilePath(fileName)
                        if(filePath != None):
                            msg = "FILE:" + fileHash
                            client.send(msg.encode("utf-8"))
                            divideFileIntoChunksAndSendChunks(client, filePath, CHUNK_SIZE)
                            break

            elif(option == "FILE"):
                try:
                    fileHash = message[1]
                    fileName = fileDict[fileHash]
                    if(fileName):
                        temp = fileName.split(".")
                        newFileName = temp[0] + "_copy" + "." + temp[1]
                        print("Waiting for the file...")
                        chunkList = []
                        file_message = client.recv(1024)
                        while file_message:
                            chunkList.append(file_message)
                            file_message = client.recv(1024)
                            file = open(newFileName, "wb")
                            for chunk in chunkList:
                                file.write(chunk)
                            file.close()
                        print("File received")
                        print("Received chunks: " + str(len(chunkList)))
                        time.sleep(0.5)
                        #client.send("FILERECEIVED".encode("utf-8"))
                        client.send("DISCONNECT".encode("utf-8"))
                        #time.sleep(0.5)
                        #connectToTargetServer(client, serverIP, port)
                        break
                except Exception as e: 
                    print(f"Error occured while receiving file: {e}")
        except ConnectionResetError:
            print("Target server has closed the connection probably due crashing, enter 0 to exit the program")
            break
        except ConnectionAbortedError:
            print("Connection to server closed, closing program..")
            break
        except Exception as e: 
            print(f"Error occured: {e}")
            fileDict.clear()
            return

# This function simply prints the names of files that are available for downloading in the network
def printFileList():
    for hash in fileDict: 
       print(fileDict[hash])
if __name__ == "__main__":
    chunk_size = 1024 # Chunk size will be approximately 1 kb (1024 bytes)
    # Specifying the information of target server
    serverIP = sys.argv[1]
    port = int(sys.argv[2])
    # Defining client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectToTargetServer(client, serverIP, port)
    isAlive = True
    username = None
    while isAlive:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectToTargetServer(client, serverIP, port)
        if(username == None):
            username = listenForNicknameStatus(client)
        threadListenServer = threading.Thread(target=listenForServerConnection, args=(client, serverIP, port))
        threadListenServer.start()
        try:
            while True:
                print("What do you want to do?")
                print("1) Print file list")
                print("2) Upload file")
                print("3) Download file")
                print("0) Exit")
                choice = input("your choice: ")
                if choice == "1":
                    # Request list of files from the target server
                    request = "FILELISTREQUEST:"
                    client.send(request.encode("utf-8"))
                    print("List of files..")
                    printFileList()

                elif choice == "2":
                    print("Upload file..")
                    print("Main choice 2:", fileDict)
                    fileName = input("Give file name: ") # This will be asked in UI later
                    uploadFile(client, username, fileName)
                elif choice == "3":
                    print("Download file..")
                    print("Main choice 3: ", fileDict)
                    request = "FILELISTREQUEST:"
                    client.send(request.encode("utf-8"))
                    fileHashList = list(fileDict.keys())
                    # This takes the first item in the list as test case
                    if(len(fileHashList) > 0):
                        fileHash = fileHashList[0]
                        requestFile(client, fileHash)  
                elif choice == "0":
                    message = "DISCONNECT:" + username
                    client.send(message.encode("utf-8"))
                    client.close()
                    isAlive = False
                    break
                else:
                    print("Read the options again and give a new choice.")
        except ConnectionResetError:
            print("Connection to target server was closed due server error")
            client.close()
        except ConnectionRefusedError and BrokenPipeError:
            client.close()
            isAlive = True
        
