import socket

host = '127.0.0.1'
port = 50008


def receiveMsg (sock, size):
  data = sock.recv(size)
  if data.decode() == "exit": return None
  return data.decode()

def sendMsg (sock,response):
  sock.sendall(response.encode())

def connection (role):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
  if role == "client" :
    sock.connect((host, port))
    print("Connected to "+(host)+" on port "+str(port))
    return sock
  if role == "server" :
    sock.bind((host, port))
    sock.listen(1)
    conn, addr = sock.accept()
    print ("Connection from", addr)
    return conn

    
  

