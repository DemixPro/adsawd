import base64
import socket
import hashlib
import threading

ClientKey = b"CK_H29DJLA23NV92MCBB09AQJ2IFV8"
EndpointKey = b"EP_AL3290OSL2390G02MSXK30GL4DA"

Socket = socket.socket()
Socket.bind(("0.0.0.0", 2896))
Socket.listen(99999)

def ClientHandle(Client, Address):
    print("Recived connection from '" + Address + "'. Authorizating...")

    if Client.recv(1024) == base64.b64encode(ClientKey):
        Client.send(EndpointKey)

        print("Sending useless data...")
        Client.send("""
print("All checks are passed, everything is works perfectly. (From endpoint, with love.)")
""")
    else:
        print("Unauthorized.")

while True:
    print("Waiting for connections...")
    Client, Address = Socket.accept()

    threading.Thread(target=ClientHandle, args=(Client, Address,)).start()
