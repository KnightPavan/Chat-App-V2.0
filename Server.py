import socket
import threading

IP = "localhost"
PORT = 1234
LIMIT = 2
CLIENTS = []

def listener(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if msg.split("~#->")[0] == "usr":
                add_client(client, msg)
        except socket.error as e:
            client.close()
            print("connection Closed")
            break
        

def add_client(client, msg):
    msg = msg.split("~#->")[1].split(",")
    userName = msg[0]
    ip = msg[1]
    port = msg[2]
    CLIENTS.append([userName,ip,port])
    client_list ='lst'+"~#->" +';'.join([f'{user[0]},{user[1]},{user[2]}' for user in CLIENTS])
    client.send(client_list.encode())
    
if __name__ =="__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((IP,PORT))
        print("Bind Success")
    except socket.error as e:
        print(e)

    server.listen(2)

    while True:
        try:
            client, addr = server.accept()
            print(f"Connection Established {addr}")
            threading.Thread(target=listener, args=(client, )).start()
        except:
            pass