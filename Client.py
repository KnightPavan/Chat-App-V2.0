import socket
import threading

IP = "localhost"
PORT = 0

SERVER_IP = "localhost"
SERVER_PORT = 1234

def server_listener(host):
    while True:
        msg = host.recv(10000).decode('utf-8')
        if msg.split("~#->")[0] == "lst":
            # print(msg)

def transfer(client, msg):
    client.send(msg.encode())

def initial_exchange(host, info):
    userName = input("Enter your username : ")
    msg = "usr"+"~#->"+ f"{userName}"+","+ f'{info[0]}'+","+ f'{info[1]}'
    transfer(host,msg)

if __name__ == "__main__":
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host.connect((SERVER_IP, SERVER_PORT))
        print("Connection TO Server Established")
    except:
        print("Unsuccessful")
    
    client.bind((IP, PORT))
    print("Bind Success")
    info = client.getsockname()
    threading.Thread(target=server_listener, args=(host, )).start()
    initial_exchange(host, info)
    
