import socket
import threading


    
class Server:

    def __init__(self, ip, port ):
        self.IP = ip
        self.PORT = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.users = []
        
    def listen(self,client,addr):
        peer = None
        while True:
            try:
                msg = client.recv(2048).decode('utf-8')
                self.msg_filter(msg, client, addr)
            except socket.error as e:
                print(str(e))

    def msg_filter(self,msg,client,addr):
        print("Filter")
        msg = msg.split("~#->")
        print(msg)
        if msg[0] == "usr":
            self.initialize(msg[1],addr)
            self.send(client,self.list_parser())
        if msg[0] == "usrlst":
            self.list_handler(client,msg[1])
        if msg[0] == "dm":
            self.dm(msg[1])

    def dm(self, msg):
        user = msg.split(">")[0]
        frm = msg.split("<")[0]
        msg = f"[{frm}]"+msg.split("<")[1]
        for i in range (0, len(self.clients)):
            if self.clients[i] == user:
                self.send(self.users[i], )

    def list_handler(self, client, username):
        if username == "0":
            self.send(client, self.list_parser())
        else:
            self.send(client, "Sermsg~#->Successfully Connected")

    def list_parser(self):
        return "lst" + "~#->" + ";".join(f'{itm[0]}' for itm in self.clients)
    
    def send(self,client, msg):
        print(msg)
        client.send(msg.encode())
    
    def initialize(self,username,addr):       
        self.clients.append([username,addr[0],addr[1]])
        print(self.clients)
    
    def initiate(self):
        
        self.server.bind((self.IP,self.PORT))
        self.server.listen()    
        
        while True:
            try:
                client, addr = self.server.accept()
                print(f"Connection established with {addr[0]}")
                threading.Thread(target=self.listen, args=(client,addr)).start()
            except:
                pass

if __name__ =="__main__":
    IP = "192.168.1.10"
    PORT = 1234
    server = Server(IP, PORT)
    server.initiate()

    