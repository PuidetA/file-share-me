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
#TODO: Implement the functions below.
# Source 1) Implementing peer-to-peer network in Python is based on this tutorial: https://www.linkedin.com/pulse/implementing-peer-to-peer-data-exchange-inpython-luis-soares-m-sc-/
# Source 2) Usage of sockets is based on this: https://www.youtube.com/watch?v=YwWfKitB8aA


#TODO: Add a list to store all the available files for sharing. i.e. fileList = []

fileList = []       # List of files available for sharing.
connectedPeers = [] # List of connected peers in the network
connectedPeer = ""  # The peer to which the client is connected.
# Based on Source 1)
class NewPeer: 
    def __init__(self, name, port):
        self.host = socket.gethostbyname(socket.gethostname())
        self.name = name
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
    def getName(self):
        return self.name
    def connectToPeer(self, peerHost, peerPort):
        try:
            newConnection = self.socket.connect((peerHost, peerPort))
            self.connections.append(newConnection)
        except socket.error as e:
            print("Failed to connect to the peer")

    def listenForNewConnections(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        while True:
            newConnection, address = self.socket.accept()
            self.connections.append(newConnection)

    def sendFile(self, file):
        for con in self.connections:
            try:
                con.sendall(file)

            except socket.error as e:
                print(f"Failed to send the file. Error: {e}")
    def start(self):
        threadForListening = threading.Thread(target=self.listenForNewConnections)
        threadForListening.start()

#   1. TODO: File Handling
def calculateFileHash(filePath):
    """
    Generates a unique hash (like SHA-1) to identify the file on the network.

    Parameters:
    - filePath: The path to the file for which the hash is to be calculated. E.g. "C:/Users/User/Documents/file.txt".

    Returns:
    - hashValue: The calculated hash value for the file. E.g. "a1b2c3d4".
    """


def divideFileIntoChunks(filePath, chunkSize):
    """
    Splits the file into smaller chunks for efficient transfer and resuming downloads.

    Parameters:
    - filePath: The path to the file to be divided into chunks. E.g. "C:/Users/User/Documents/file.txt".
    - chunkSize: The size (in bytes) of each chunk. E.g. 1024 bytes.

    Returns:
    - chunkPaths: A list containing the paths to the generated chunks. E.g. ["C:/Users/User/Documents/file_chunk1.txt", "C:/Users/User/Documents/file_chunk2.txt"].
    """


def reassembleFile(fileHash):
    """
    Combines chunks into the complete file after downloading.

    Parameters:
    - fileHash: The hash value identifying the file. E.g. "a1b2c3d4".

    Returns:
    - filePath: The path to the reassembled file. E.g. "C:/Users/User/Documents/file.txt".
    """



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
def registerPeer(name, port):
    """
    Register a peer with name and port number.
    Both sides have to do it (or only one depending on implementation. Either works.).
    Parameters: name, port

    Returns: None
    """
    hostSocket = NewPeer(name, port)
    hostSocket.start()
    connectedPeers.append(hostSocket)
    print("Peer registered successfully!")
    return hostSocket

def connectToPeer(hostSocket, name):
    # Find the peer from the list (In this case, we have only two connected clients but this would be scalable for more than two users if implemented in this way)
    print("Trying to find the requested peer..")
    for peer in connectedPeers:
        if (peer.getName() == name):
            print("Opening connection..")
            hostSocket.sendFile(hostSocket, )


def unregisterPeer(name):
    """
    Unregister the current peer. i.e. make the connectedPeer = "".

    Parameters: name

    Returns: None
    """
    for peer in connectedPeers:
        if(peer.getName() == name):
            peer.socket.close()
            connectedPeers.remove(peer)



#   4. TODO: File Exchange
def requestChunk(fileHash, chunkIndex):
    """
    Send a request to a peer.

    Parameters:
    - fileHash: The hash value identifying the file for which the chunk is requested. E.g. "a1b2c3d4".
    - chunkIndex: The index of the chunk requested. E.g. 0.

    Returns: None
    """

def sendChunk(fileHash, chunkIndex, chunkData):
    """
    Send a chunk in response.

    Parameters:
    - fileHash: The hash value identifying the file for which the chunk is sent. E.g. "a1b2c3d4".
    - chunkIndex: The index of the chunk being sent. E.g. 0.
    - chunkData: The data of the chunk being sent.

    Returns: None
    """

def downloadFile(fileHash):
    """
    Get peer list, coordinate requests, and reassemble chunks.

    Parameters:
    - fileHash: The hash value identifying the file to be downloaded. E.g. "a1b2c3d4".

    Returns: None
    """
    fileIndex = fileList.index(fileHash)
    if (ValueError):
        print("File is not available to share")
        return
    else:
        downloadedFile = fileList[fileIndex]
def choices():
    print("What would you like to do?")
    print("1) Send file to peer")
    print("0) End program")
    choice = int(input("Give your choice: "))
    return choice

def main():
    port = int(sys.argv[1])
    # Specifying the new user as part of peer network
    username = input("Give your username: ")
    hostSocket = registerPeer(username, port)
    while(True):
        choice = choices()
        if(choice == 1):
            peerName = input("Who you want to download file from: ")
            connectToPeer(hostSocket, peerName)
        elif(choice == 0):
            unregisterPeer(username)
            print("Closing program, thank you..")
            break
    

main()    
#TODO: Add in the functions from above to the main below to make them work.
# Main
if __name__ == "__main__":
    pass