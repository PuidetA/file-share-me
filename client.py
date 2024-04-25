
"""
Interaction Example: Downloading a File

1. Request and receive file list: User requests the network for current list. displayFileList() queries the network.
2. UI Update: displayFileList() shows search results to the user.
3. Download Initiation: User approves file download. requestFile(fileHash) starts.
4. Connection and Requests: connectToTargetServer() establishes connection to target server that handles the requests and transferring files between clients

"""
"""NEW Client-Side Functionality:

Reason for simplified design: The initial design was too complex for the given amount of time. The new design focuses on the core functionalities needed for a basic file-sharing system.
The focus will be more on P2P sharing between only 2 systems. The client will handle file management, peer management, and file exchange.

1. File Handling

calculateFileHash(filePath): Generates a unique hash (like SHA-1) to identify the file on the network.
divideFileIntoChunksAndSendChunks(filePath, chunkSize): Splits the file into smaller chunks for efficient transfer and resuming downloads.

2. User Interface (UI):

displayFileList(): Updates the UI with the list of files available for download from other peer.
updateFileList(): Updates the file list to reflect new files that are added to the folder.
shareFileList(fileList): Triggered when displayFileList() function from another peer requests a list of files.
updateDownloadProgress(fileHash, progress): Visually displays download progress of a file (or how many chunks are left to be downloaded).


3. File Exchange

requestFile(fileHash): Send a request to a peer.
sendChunk(peerID, fileHash, chunkIndex, chunkData): Send a chunk in response.
downloadFile(fileHash): Get peer list, coordinate requests, and reassemble chunks.

Sources for this code: 
1) 


"""




import hashlib # Can be used for generating hash values.
import os # Can be used for file operations.
import tkinter as tk #Tkinter is a standard library used for GUI development.
from tkinter import ttk # for tkinter widget in charge of making a treeview
import customtkinter as ctk #For modernized tkinter GUI
from tkinter import filedialog #For local directory selection
import sv_ttk #credit to: rdbende from github for the ttk theme.

import sys
import time
import random
import socket
import threading
#TODO: Implement the functions below.
# Source 1) How to use sockets is done based on this video: https://www.youtube.com/watch?v=YwWfKitB8aA
# Source 2) Sending and receiving chunks of file with TCP connection in Python is based on this: https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
# Source 3) 
#+ Documentations of each used library :D

fileDict = {}       # Dictionary of files available for sharing. Form: hash value of the file as key and fileName as value
isAlive = True
CHUNK_SIZE = 1024 # Chunk size will be approximately 1 kb (1024 bytes)
chunkPaths = []
currentFileDirectory = ""
username = None


# Defining client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
            #client.close()
            print("File send to the server")
            #time.sleep(3)
            #newClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #connectToTargetServer(newClient, serverIP, port)
    except FileNotFoundError:
        print("Check the file name and try again")
    except Exception as e: 
        print(f"Try again, error: {e}")

#def reassembleFile(fileHash, fileName, chunkPaths):
    """
    Combines chunks into the complete file after downloading.

    Parameters:
    - fileHash: The hash value identifying the file. E.g. "a1b2c3d4".

    Returns:
    - filePath: The path to the reassembled file. E.g. "C:/Users/User/Documents/file.txt".
    """



#   2. TODO: User Interface (UI)


def displayCurrentFileList(givenDirectoryPath, listbox):
# This function tries to find the path of file by its name 

    currentFileDirectory = givenDirectoryPath
    listbox.delete(0, 'end') #Clears the listbox before adding files to it. This is to ensure that only the files in the selected directory are displayed. (also to avoid duplicating the same directory if the user runs the command multiple times.)
    #testList = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"] #Test list of files for sharing
    files=[file for file in os.listdir(givenDirectoryPath) if os.path.isfile(os.path.join(givenDirectoryPath, file))]
    for file in files: #Get files and insert them into the listbox. Uncomment testList and replace "files" with "testList" if you want to test the function without having to select a directory.
        listbox.insert('end', file)


def getFilePath(fileName):
    try:
        if(fileName):
            #current_directory = os.getcwd() + "\\files"
            #path = os.path.join(current_directory, fileName)
            path = os.path.join(currentFileDirectory, fileName)
            return path
        else: 
            return None
    except FileNotFoundError as e:
        print(f"File not found: {e}")

    

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

def main():
    """
    Main function to handle the user interface and file sharing operations.

    Parameters: None

    Returns: None
    """
    global root # This will be the main window. It is global so that other functions can use it. e.g. exitProgram() function.
    root = ctk.CTk() #root/main window
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
    commandFrame.grid_rowconfigure(18, weight=1) #Configures the row of the commandFrame

    ## commandFrame widgets
    #Section covers the intro text and places it in the commandFrame at the top
    introText = ctk.CTkLabel(commandFrame, text="File Sharing Application Text", corner_radius=10)
    introText.grid(row=0, column=0)



    #Section covers the connect button and the entry widgets for the IP address and port number
    connectInstructionText = ctk.CTkLabel(commandFrame, text="Enter IP address and port number to connect to")
    connectInstructionText.grid(row=1, column=0)
    connectEntryIP = ctk.CTkEntry(commandFrame, placeholder_text="IP Address")
    connectEntryIP.grid(row=2, column=0, pady=1)
    connectEntryPort = ctk.CTkEntry(commandFrame, placeholder_text="Port Number")
    connectEntryPort.grid(row=3, column=0)
    connectButton = ctk.CTkButton(commandFrame, text="Connect", command=lambda: registerPeer(connectEntryIP.get(), connectEntryPort.get()))
    connectButton.grid(row=4, column=0, pady=10)

    #Section covers the username entry widget
    usernameInstructionText = ctk.CTkLabel(commandFrame, text="Please enter your username")
    usernameInstructionText.grid(row=5, column=0)
    usernameEntry = ctk.CTkEntry(commandFrame, placeholder_text="Enter username")
    usernameEntry.grid(row=6, column=0)
    usernameButton = ctk.CTkButton(commandFrame, text="Enter", command=lambda: listenForNicknameStatus(client))
    usernameButton.grid(row=7, column=0, pady=2)


    #Section covers:
    #1. The "Absolute file path" entry widget to paste the absolute path to the local directory.
    #2. The "Select directory" button which runs commands that let you choose a directory from your computer and pastes it into the entry widget (it clears the text box before pasting).
    #3. The "Enter" button to get the absolute directory path from the entry widget and display the files via displayCurrentFileList(*) function.
    filepathInstructionText = ctk.CTkLabel(commandFrame, text="Enter the path of the file folder to select and view")
    filepathInstructionText.grid(row=8, column=0)
    filepathEntry = ctk.CTkEntry(commandFrame, placeholder_text="Absolute file path")
    filepathEntry.grid(row=9, column=0)
    #File selection button - opens a file dialog to select a file
    filepathEntryDirectorySelectButton = ctk.CTkButton(commandFrame, text="Select directory", command=lambda: selectLocalDirectory(filepathEntry)) 
    filepathEntryDirectorySelectButton.grid(row=10, column=0, pady=2)
    selectButton = ctk.CTkButton(commandFrame, text="Enter", command=lambda: displayCurrentFileList(filepathEntry.get(), listbox))
    selectButton.grid(row=11, column=0, pady=10)





    #Upload and Download file instructions
    uploadDownloadInstructionText = ctk.CTkLabel(commandFrame, text="Select a file to upload or download")
    uploadDownloadInstructionText.grid(row=12, column=0)


    #Section covers the "Download" button that will be used to download the selected file
    downloadEntry = ctk.CTkEntry(commandFrame, placeholder_text="Download file name")
    downloadEntry.grid(row=13, column=0)
    downloadButton = ctk.CTkButton(commandFrame, text="Download", command=lambda: requestFile(client, fileHash))
    downloadButton.grid(row=14, column=0, pady=2)


    #Section covers the "Upload" button that will be used to upload the selected file
    uploadEntry = ctk.CTkEntry(commandFrame, placeholder_text="Upload file name")
    uploadEntry.grid(row=15, column=0, pady=2)
    uploadButton = ctk.CTkButton(commandFrame, text="Upload", command=lambda: uploadFile(client, username, fileName))
    uploadButton.grid(row=16, column=0)




    #Section covers the "Exit" button that will be used to exit the program
    exitButton = ctk.CTkButton(commandFrame, fg_color="red", text="Disconnect & Exit", command=exitProgram)
    exitButton.grid(row=17, column=0, pady=20)



    ### resultsFrame

    resultsFrame=ctk.CTkFrame(root, width=200, height=400, corner_radius=10) #Frame in which the files are displayed TODO: Insert it and implement the displayCurrentFileList() function
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

def enterUsername(usernameEntry):
    status = "INVALID"
    username = usernameEntry


    client.send(username.encode("utf-8"))
    status = client.recv(1024).decode("utf-8")
    if(status == "VALID"):
        sendFileNamesToServer(client, username)
    else:
        print("Error: Invalid username, try again")
        username = None
    

def registerPeer(serverIP, port):
    serverIP = sys.argv[1]
    port = int(sys.argv[2])
    connectToTargetServer(client, serverIP, port)

def exitProgram():
    client.close()
    message = "DISCONNECT:" + username
    client.send(message.encode("utf-8"))
    client.close()
    root.destroy()
    
    
    

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
# This function listens for messages that are coming from the server and responds to them
# based on the options it has which are FILELIST, UPLOAD, NEWFILE, FILESENDREQUEST, FILE


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

def listenForServerConnection(client, serverIP, port):
    """
    messages server can be received from the target server:
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

#TODO: Add in the functions from above to the main below to make them work.
# Main
def printFileList():
    print(fileDict)
    index = 0
    for hash in fileDict: 
       print(fileDict[hash], index)
       index = index + 1



       
if __name__ == "__main__":



    main() # Main function that starts the GUI via a mainloop. This will loop until the program is stopped (there is no break from the loop).



    
    """# Specifying the new user as part of peer network
    serverIP = sys.argv[1]
    port = int(sys.argv[2])"""
    #username = input("Give your username: ")
    # Defining client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectToTargetServer(client, serverIP, port)

    while isAlive:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectToTargetServer(client, serverIP, port)
        if(username == None):
            username = listenForNicknameStatus(client)
        threadListenServer = threading.Thread(target=listenForServerConnection, args=(client, serverIP, port))
        threadListenServer.start()
        try:
            while True:
                print("What do you want to do?") # Comments to list off functions done by UI in main()
                print("1) Print file list") #done
                print("2) Upload file")
                print("3) Download file") #done
                print("0) Exit") #done
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
        except ConnectionRefusedError and BrokenPipeError:
            #print("Connection closed, closing the program")
            client.close()
            isAlive = True
        
