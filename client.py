"""OLD: Client-Side Functionality
1. File Handling

calculateFileHash(filePath): Generates a unique hash (like SHA-1) to identify the file on the network.
divideFileIntoChunks(filePath, chunkSize): Splits the file into smaller chunks for efficient transfer and resuming downloads.


2. User Interface (UI)

onDragEnter(): Handles when a user drags a file into the designated area.
onDragLeave(): Handles when the dragged file leaves the drop area.
onDrop(filePath): Triggered when the file is dropped. Initiates calculateFileHash() and prepares for sharing.
displayFileList(): Updates the UI with the list of files available for download.
shareFileList(fileList): Triggered when displayFileList() method from another peer requests a list of files.
updateDownloadProgress(fileHash, progress): Visually displays download progress of a file.


3. Peer Discovery and Connection

connectToSharingNetwork(*clientAddresses): Establishes a connection to the file sharing network.
registerWithNetwork(fileHash, clientID): Informs the network that this client is sharing a particular file.
sharePeerList(fileHash): Retrieves a list of healthy peers with the desired file.
connectToPeer(peerAddress, peerPort): Establishes a direct TCP connection with another peer.


4. File Transfer

requestFileChunk(peerID, fileHash, chunkIndex): Sends a request to a peer for a specific chunk of a file.
sendFileChunk(peerID, fileHash, chunkIndex, chunkData): Responds to a chunk request by sending the actual file data.
receiveFileChunk(peerID, fileHash, chunkIndex, chunkData): Function to receive a chunk, verify its integrity, and store it.


5. Download/Upload Management

initiateDownload(fileHash): After approving download of a file, begins the download process by fetching the peer list of healthy peers that have the file and starting connections.
prioritizePeers(): Selects the most suitable peers based on factors like download speed and availability of chunks.
reassembleFile(fileHash): Once all chunks are downloaded, reassembles the file.


"""

"""
Interaction Example: Downloading a File

1. Request and receive file list: User requests the network for current list. displayFileList() queries the network.
2. UI Update: displayFileList() shows search results to the user.
3. Download Initiation: User approves file download. initiateDownload(fileHash) starts.
4. Peer Retrieval: sharePeerList() gets peers.
5. Connection and Requests: connectToPeer() establishes connections, then requestFileChunk() is sent to multiple peers.
6. Chunk Transfer: Peers use sendFileChunk() to respond. The client uses receiveFileChunk() to get data.
7. Optimization: prioritizePeers() runs to prefer better sources.
8. Reassembly: reassembleFile() combines chunks into the complete file.

"""


"""NEW Client-Side Functionality:

Reason for simplified design: The initial design was too complex for the given amount of time. The new design focuses on the core functionalities needed for a basic file-sharing system.
The focus will be more on P2P sharing between only 2 systems. The client will handle file management, peer management, and file exchange.

1. File Handling

calculateFileHash(filePath): Generates a unique hash (like SHA-1) to identify the file on the network.
divideFileIntoChunks(filePath, chunkSize): Splits the file into smaller chunks for efficient transfer and resuming downloads.
reassembleFile(fileHash): Combines chunks into the complete file after downloading.

2. User Interface (UI):

displayFileList(): Updates the UI with the list of files available for download from other peer.
updateFileList(): Updates the file list to reflect new files that are added to the folder.
shareFileList(fileList): Triggered when displayFileList() method from another peer requests a list of files.
updateDownloadProgress(fileHash, progress): Visually displays download progress of a file (or how many chunks are left to be downloaded).


3. Peer Management

registerPeer(): Register a peer with given IP address and port number. Both sides have to do it (or only one depending on implementation. Either works.) You can only register one peer right now. (we can add more later on like folder specific peer)
unregisterPeer(): Unregister the current peer.


4. File Exchange

requestChunk(peerID, fileHash, chunkIndex): Send a request to a peer.
sendChunk(peerID, fileHash, chunkIndex, chunkData): Send a chunk in response.
downloadFile(fileHash): Get peer list, coordinate requests, and reassemble chunks."""


import hashlib # Can be used for generating hash values.
import os # Can be used for file operations.
import sys
import socket
import threading
from pysondb import db
#TODO: Implement the functions below.
# Source 1) Implementing peer-to-peer network in Python is based on this tutorial: https://www.linkedin.com/pulse/implementing-peer-to-peer-data-exchange-inpython-luis-soares-m-sc-/
# Source 2) Usage of sockets is based on this: https://www.youtube.com/watch?v=YwWfKitB8aA
# Source 3) Getting public ip address: https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python

#TODO: Add a list to store all the available files for sharing. i.e. fileList = []

fileDict = {}       # List of files available for sharing.
connectedPeers = [] # List of connected peers in the network
connectedPeer = ""  # The peer to which the client is connected.
isAlive = False
# Based on Source 1)

filesDB = db.getDb("filesDB.json")

#   1. TODO: File Handling
def calculateFileHash(filePath):
    """
    Generates a unique hash (like SHA-1) to identify the file on the network.

    Parameters:
    - filePath: The path to the file for which the hash is to be calculated. E.g. "C:/Users/User/Documents/file.txt".

    Returns:
    - hashValue: The calculated hash value for the file. E.g. "a1b2c3d4".
    """
        # Initializing the sha1() method
    sha1 = hashlib.sha1()

    # Passing the byte stream as an argument
    sha1.update(filePath)

    # Make a hexadecimal form hash of the given byte stream
    hashValue = sha1.hexdigest()
    print(hashValue)

    # Source 2:
    with open(filePath, "rb") as file: 
        digest = hashlib.file_digest(file, "sha254")
    
    hashValue = digest.hexdigest() 
    
    return hashValue


def divideFileIntoChunks(filePath, chunkSize):
    """
    Splits the file into smaller chunks for efficient transfer and resuming downloads.

    Parameters:
    - filePath: The path to the file to be divided into chunks. E.g. "C:/Users/User/Documents/file.txt".
    - chunkSize: The size (in bytes) of each chunk. E.g. 1024 bytes.

    Returns:
    - chunkPaths: A list containing the paths to the generated chunks. E.g. ["C:/Users/User/Documents/file_chunk1.txt", "C:/Users/User/Documents/file_chunk2.txt"].
    """
    chunkPaths = []

    file = open(filePath, "rb")
    chunk = 0
    byte = file.read(chunkSize) 
    while byte:
        
        file_temp = "chunk" + str(chunk) + ".txt"
        file_chunk = open(file_temp, "wb")
        file_chunk.write(byte)
        file_chunk.close()
        
        current_directory = os.getcwd()
        chunk_path = os.path.join(current_directory, file_temp)

        # Tehdäänkö hash tässä vaiheessa vai jossain muualla?
        # chunk_path_hashed = calculateFileHash(chunk_path)
        chunkPaths.append(chunk_path)
            
        byte = file.read(chunkSize)
         
        chunk += 1
    return chunkPaths


def reassembleFile(fileHash, chunkPaths):
    """
    Combines chunks into the complete file after downloading.

    Parameters:
    - fileHash: The hash value identifying the file. E.g. "a1b2c3d4".

    Returns:
    - filePath: The path to the reassembled file. E.g. "C:/Users/User/Documents/file.txt".
    """
    file_name = "imageCopy.png" # Kovakoodattu :D Kato miten menee lopullisessa työssä
    current_directory = os.getcwd()
    path_reassembled = os.path.join(current_directory, file_name)
    file_reassembled = open(path_reassembled, "ab")
    # chunks_reassembled = None
    
    # Read the file chunks into one string
    for chunk_path in chunkPaths:
        file_chunk = open(chunk_path, "rb")
        byte = file_chunk.read(1024)
        file_reassembled.write(byte)
        # chunks_reassembled += file_chunk
        file_chunk.close()
    
    # Write the string into a file
    # file_reassembled.write(chunks_reassembled)
    file_reassembled.close()
    filePath = file_reassembled 
    return filePath

#   2. TODO: User Interface (UI)
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


#   3. TODO: Peer Management (Aino)
# NewPeer class is going to be used and is based on source 1!
def registerPeer(name, ip, port):
    """
    Register a peer with name and port number.
    Both sides have to do it (or only one depending on implementation. Either works.).
    Parameters: name, port

    Returns: None
    """
    #hostSocket = NewPeer(name, ip, port)
    #hostSocket.start()
    #connectedPeers.append(hostSocket)
    #print("Peer registered successfully!")
   # return hostSocket

def unregisterPeer(name):
    """
    Unregister the current peer. i.e. make the connectedPeer = "".
    Parameters: name
    Returns: None
    """
    #for peer in connectedPeers:
     #   if(peer.getName() == name):
      #      peer.socket.close()
       #     connectedPeers.remove(peer)


#   4. TODO: File Exchange
def requestFile(client, username, fileName):
    """
    Send a request to the tracker server.
    """
    message = "REQUEST:" + username + ":" + fileName
    client.send(message.encode("utf-8"))

def sendChunk(fileHash, chunkIndex, chunkData):
    """
    Send a chunk in response.

    Parameters:
    - fileHash: The hash value identifying the file for which the chunk is sent. E.g. "a1b2c3d4".
    - chunkIndex: The index of the chunk being sent. E.g. 0.
    - chunkData: The data of the chunk being sent.

    Returns: None
    """

def downloadFile(client, username, fileName):      
    requestFile(client, username, fileName)

    #connectToPeer(fileHash)
def uploadFile(client, username, fileName):
    #calculateFileHash()
    #hash ="asmiwfmiaxbuj"
    fileHash = calculateFileHash()
    request = "UPLOADREQUEST:" + fileHash + ":" + username + ":" + fileName
    client.send(request.encode("utf-8"))
    #file = {"hash": hash, "owner": username, "fileName": fileName}

    #filesDB.add(file)
    #Here client uploads the name of file they have which is stored to filesDB. 

def connectToTargetServer(client, address, port):
    try:
        client.connect((address, port))
        client.send(bytes(username, "utf-8"))
    except Exception as e: 
        print("Exception occurred {e}")

def listenForServerConnection(client, username):
    while isAlive:
        try: 
            message = client.recv(1024).decode("utf-8")
            #if(message == "FILEREQUEST"):
                
             #   client.send(bytes(username, "utf-8"))

            #elif():
        except Exception as e: 
            print(e)

#TODO: Add in the functions from above to the main below to make them work.
# Main


if __name__ == "__main__":
    chunk_size = 1024 # Chunk size will be approximately 1 kb (1024 bytes)
    chunkPaths = []
    #hostIP = str(sys.argv[1])
    #port = int(sys.argv[2])
    # Specifying the new user as part of peer network
    serverIP = sys.argv[1]
    port = int(sys.argv[2])
    fileDict = {"hash1": ["image.png", "peername1"], "hash2": ["start.png", "peername2"]}
    username = input("Give your username: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectToTargetServer(client, serverIP, port)
    thread = threading.Thread(target=listenForServerConnection, args=(client, username))
    thread.start()
    isAlive = True
    while True:
        print("What do you want to do?")
        print("1) Print file list")
        print("2) Upload file")
        print("3) Download file")
        print("0) Exit")
        choice = input("your choice: ")
        if choice == "1":
            print("List of files..")
        elif choice == "2":
            print("Upload file..")
            fileName = input("Give file name: ")
            uploadFile()
        elif choice == "3":
            print("Download file..")
            fileName = input("Give file name: ")
            downloadFile(client, username, fileName)
        
         #   # file = input("Give name of the file you want to save the fixed file as: ")
          #  filePath = reassembleFile(chunkPaths)
           # print(filePath)
            
        
        elif choice == "0":
         #   unregisterPeer(username)
            isAlive = False
            print("Thank you for using this very cool app.")
            break
        else:
            print("Read the options again and give a new choice.")