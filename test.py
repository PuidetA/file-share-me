import socket
import threading

#HOST = "86.50.47.211"
#socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.create_server(HOST)
socket = socket.create_connection(("86.50.40.18", 12345))
socket.send(b"Hello!")