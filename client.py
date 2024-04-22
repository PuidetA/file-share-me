"""OLD: Client-Side Functionality
1. File Handling

calculateFileHash(filePath): Generates a unique hash (like SHA-1) to identify the file on the network.
divideFileIntoChunks(filePath, chunkSize): Splits the file into smaller chunks for efficient transfer and resuming downloads.


2. User Interface (UI)

onDragEnter(): Handles when a user drags a file into the designated area.
onDragLeave(): Handles when the dragged file leaves the drop area.
onDrop(filePath): Triggered when the file is dropped. Initiates calculateFileHash() and prepares for sharing.
displayFileList(): Updates the UI with the list of files available for download.
shareFileList(fileList): Triggered when displayFileList() function from another peer requests a list of files.
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
shareFileList(fileList): Triggered when displayFileList() function from another peer requests a list of files.
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
import tkinter as tk #Tkinter is a standard library used for GUI development.
from tkinter import ttk # for tkinter widget in charge of making a treeview
import customtkinter as ctk #For modernized tkinter GUI
from tkinter import filedialog #For local directory selection
import sv_ttk #credit to: rdbende from github for the ttk theme.

#TODO: Implement the functions below.



#TODO: Add a list to store all the available files for sharing. i.e. fileList = []

fileList = []       # List of files available for sharing.
connectedPeer = ""  # The peer to which the client is connected.

testPath = "" #Test path for the locally stored files


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
def displayFileList(givenDirectoryPath, listbox):
    """
    Updates the UI with the list of files available for download from other peers. E.g. displays a list of files in a window.

    Parameters: fileList e.g. ["file1.txt", "file2.txt"]

    Returns: None
    """
    listbox.delete(0, 'end') #Clears the listbox before adding files to it. This is to ensure that only the files in the selected directory are displayed. (also to avoid duplicating the same directory if the user runs the command multiple times.)
    #testList = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"] #Test list of files for sharing
    files=[file for file in os.listdir(givenDirectoryPath) if os.path.isfile(os.path.join(givenDirectoryPath, file))]
    for file in files: #Get files and insert them into the listbox. Uncomment testList and replace "files" with "testList" if you want to test the function without having to select a directory.
        listbox.insert('end', file)
    

def updateFileList():
    #TODO: rewrite this. Requirements changed. This functionality needs to exist, but the implementation will be different.
    """
    Updates the file list to reflect new files that are added to the folder. i.e. a button that triggers the update and adds it to fileList = [].

    Parameters: None

    Returns: None
    """

def shareFileList(fileList):
    #TODO: rewrite this. Requirements changed. This functionality needs to exist, but the implementation will be different.
    """
    Triggered when displayFileList() function from another peer requests a list of files.

    Parameters:
    - fileList: The list of files available for sharing. E.g. ["file1.txt", "file2.txt"].

    Returns: None
    """

def updateDownloadProgress(fileHash, progress): 
    #TODO: rewrite this. Requirements changed. This functionality needs to exist, but the implementation will be different.
    """
    
    Visually displays download progress of a file (or how many chunks are left to be downloaded).

    Parameters:
    - fileHash: The hash value identifying the file being downloaded. E.g. "a1b2c3d4".
    - progress: The download progress, indicating how many chunks are left to be downloaded. E.g. 5/64 chunks downloaded. In the terminal, it can be displayed as "Downloading file: 5/64".

    Returns: None
    """

def main():
    """
    Main function to handle the user interface and file sharing operations.

    Parameters: None

    Returns: None
    """
    root=ctk.CTk() #root/main window
    ctk.set_appearance_mode("dark") #Sets the appearance mode of the GUI to dark
    ctk.set_default_color_theme("green") #Sets the default color theme of the GUI elements to green
    root.title("File Sharing Application") #Title of the window
    root.geometry("800x600") #Size of the window



    #Configuring the grid layout of the window. It is a 4x4 grid.
    root.grid_columnconfigure(1, weight=1)
    #root.grid_columnconfigure((2, 3), weight=0)
    root.grid_columnconfigure(4, weight=1)
    root.grid_rowconfigure((0, 1, 2), weight=1)

    ### commandFrame

    commandFrame=ctk.CTkFrame(root, width=140, corner_radius=0) #Frame in which the command buttons and entries are placed in
    commandFrame.grid(row=0, column=0, sticky="nsew", rowspan=4) #Places the commandFrame in the main window
    commandFrame.grid_rowconfigure(12, weight=1) #Configures the row of the commandFrame

    ## commandFrame widgets
    #Section covers the intro text and places it in the commandFrame at the top
    introText = ctk.CTkLabel(commandFrame, text="File Sharing Application Text", corner_radius=10)
    introText.grid(row=0, column=0)

    #Section covers the connect button and the entry widgets for the IP address and port number
    connectInstructionText = ctk.CTkLabel(commandFrame, text="Enter IP address and port number to connect to")
    connectInstructionText.grid(row=1, column=0)
    connectEntryIP = ctk.CTkEntry(commandFrame, placeholder_text="IP Address")
    connectEntryIP.grid(row=2, column=0)
    connectEntryPort = ctk.CTkEntry(commandFrame, placeholder_text="Port Number")
    connectEntryPort.grid(row=3, column=0)
    connectButton = ctk.CTkButton(commandFrame, text="Connect", command=registerPeerButton)
    connectButton.grid(row=4, column=0, pady=10)


    #Section covers:
    #1. The "Absolute file path" entry widget to paste the absolute path to the local directory.
    #2. The "Select directory" button which runs commands that let you choose a directory from your computer and pastes it into the entry widget (it clears the text box before pasting).
    #3. The "Enter" button to get the absolute directory path from the entry widget and display the files via displayFileList(*) function.
    filepathInstructionText = ctk.CTkLabel(commandFrame, text="Enter the path of the file to select and view")
    filepathInstructionText.grid(row=5, column=0)
    filepathEntry = ctk.CTkEntry(commandFrame, placeholder_text="Absolute file path")
    filepathEntry.grid(row=6, column=0)
    #File selection button - opens a file dialog to select a file
    filepathEntryDirectorySelectButton = ctk.CTkButton(commandFrame, text="Select directory", command=lambda: selectLocalDirectory(filepathEntry)) 
    filepathEntryDirectorySelectButton.grid(row=7, column=0, pady=2)
    selectButton = ctk.CTkButton(commandFrame, text="Enter", command=lambda: displayFileList(filepathEntry.get(), listbox))
    selectButton.grid(row=8, column=0, pady=10)



    ### resultsFrame

    resultsFrame=ctk.CTkFrame(root, width=200, height=400, corner_radius=10) #Frame in which the files are displayed TODO: Insert it and implement the displayFileList() function
    resultsFrame.grid(row=0, column=4, sticky="NESW", rowspan=4, columnspan=2) #Places the resultsFrame in the main window
    resultsFrame.grid_rowconfigure(4, weight=3) #Configures the row of the resultsFrame

    ## resultsFrame widgets 
    
    #Listbox widget for displaying the files
    listbox = tk.Listbox(resultsFrame)
    listbox.pack(side='left', fill='both', expand=True)

    # Scrollbar widget for the listbox widget that allows the user to scroll through the list
    scrollbar = ttk.Scrollbar(resultsFrame, orient='vertical', command=listbox.yview)
    scrollbar.pack(side='right', fill='y')
    # Configure listbox to use scrollbar by setting the yscrollcommand option
    listbox['yscrollcommand'] = scrollbar.set


    ### Set theme to Sun Valley. Mostly for the scrollbar and listbox widgets.
    sv_ttk.set_theme("dark") 

    ### Starts the UI (mainloop)
    root.mainloop()

def selectLocalDirectory(filepathEntry):
    """
    Function to select a local directory for file sharing.

    Parameters: filepathEntry - Entry widget for the file path.

    Returns: Absolute path of the selected directory.
    """
    directoryPath = filedialog.askdirectory() #Opens a dialog box to select a directory and assigns the selected directory to directoryPath
    if directoryPath:  # Check if a directory was selected
        filepathEntry.delete(0, tk.END)  # Clear existing content in the entry
        filepathEntry.insert(0, directoryPath)  # Insert the new path


    """directoryPath = filedialog.askdirectory() #Opens a dialog box to select a directory and assigns the selected directory to directoryPath
    return directoryPath"""


def registerPeerButton(): #Function to handle the connect button
    pass
    registerPeer(connectEntryIP.get(), connectEntryPort.get()) #Calls the registerPeer function with the IP and port number entered by the user via entryWidgetName.get()
    




#   3. TODO: Peer Management
def registerPeer():
    """
    Register a peer with given IP address and port number.
    Both sides have to do it (or only one depending on implementation. Either works.).
    You can only register one peer right now. (we can add more later on like folder specific peer)

    Parameters: None

    Returns: None
    """

def unregisterPeer():
    """
    Unregister the current peer. i.e. make the connectedPeer = "".

    Parameters: None

    Returns: None
    """




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



#TODO: Add in the functions from above to the main below to make them work.
# Main
if __name__ == "__main__":
    main()