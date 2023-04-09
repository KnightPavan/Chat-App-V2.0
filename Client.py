import socket
import threading

IP = "192.168.1.10" #change
PORT = 0
CLIENT_LIST=[]
SERVER_IP = "192.168.1.10"
SERVER_PORT = 1234

def server_listener(host):
    while True:
        msg = host.recv(10000).decode('utf-8')
        if msg.split("~#->")[0] == "lst":
            option_select(msg[7:])

def client_listner(client):
    while True:
        try:
            print(client.recv(2048).decode('utf-8'))
        except:
            pass
def client_sender(client):
    while True:
        msg= input(">>>")
        transfer(client, msg)

def option_select(msg):
    lst = msg.split(";")
    lst = [user.split(",") for user in lst]
    # print(lst)
    print("Active Users")
    print(lst)
    for user in lst:
        CLIENT_LIST.append([user[0],user[1],user[2]])
        print(user[0])
    print("0 : Wait for Message")
    User = input("Enter the user you want connect : ")
    if (User == "0"):
        print("Waiting for connection")
        pass
    else:
        for user in lst:
            if user[0] == User:
                connect_client(user[0],user[1],int(user[2]))
    
def connect_client(UserName,ip,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(port)
    while True:
        try:
            client.connect((ip,port))
            print("connection Established with ",UserName)
            threading.Thread(target=client_listner, args=(client, )).start()
            threading.Thread(target=client_sender, args=(client, )).start()
            break
        except:
            print("Error")
    
    

def transfer(client, msg):
    client.send(msg.encode())

def initial_exchange(host, info, port):
    userName = input("Enter your username : ")
    msg = "usr"+"~#->"+ f"{userName}"+","+ f'{IP}'+","+ f'{port}'
    transfer(host,msg)

if __name__ == "__main__":
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host.connect((SERVER_IP, SERVER_PORT))
        addr = host.recv(2048).decode('utf-8')
        print(addr)
        print("Connection TO Server Established")
    except:
        print("Unsuccessful")
    print(host)
    print(server)
    server.bind((IP, int(addr.split(":")[1])))
    print("Bind Success")
    info = server.getsockname()
    # print(info)
    threading.Thread(target=server_listener, args=(host, )).start()
    initial_exchange(host, info, int(addr.split(":")[1]))
    server.listen(2)
    while True:
        try:
            client, addr = server.accept()
            print("Accetped to message")
            threading.Thread(target=client_listner, args=(client, )).start()
            threading.Thread(target=client_sender, args=(client, )).start()
            break
        except:
            pass
    
        

    
