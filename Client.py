import socket
import threading

class Client:
    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
        self.host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ""

    def send(self,msg):
        print("MSG Sent")
        self.host.send(msg.encode())
    
    def listen(self):
        while True:
            try:
                msg = self.host.recv(2048).decode('utf-8')
                self.msg_filter(msg)
            except:
                pass
    def msg_filter(self, msg):
        msg = msg.split("~#->")
        if msg[0] == "lst":
            self.user_list(msg[1])
        elif msg[0] == "Sermsg":
            print(msg[1])

    def user_list(self, list):
        list = list.split(";")
        print("List of Users on the server")
        for usr in list:
            print(usr)
        print("0 : To reload user list")
        msg = input("Enter the username : ")
        msg = "usrlst" +"~#->"+ msg
        self.send(msg)
        

    def initiate(self):
        while True:
            try:
                self.host.connect((self.IP, self.PORT))
                threading.Thread(target=self.listen, args=()).start()
                self.send(self.initialize())
                
                break
            except:
                pass

    def initialize(self):
        self.username = input("USERNAME : ") 
        return "usr" + "~#->" + self.username
    
if __name__ == "__main__":
    IP = "192.168.1.10"
    PORT = 1234
    client = Client(IP, PORT) 
    client.initiate()

    
        

    
