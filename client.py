import socket
 
host = '192.168.218.139'
port = 50010
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Connected to "+(host)+" on port "+str(port))
initialMessage = input("Send: ")
s.sendall(initialMessage.encode())
 
while True:
 data = s.recv(1024)
 print("Recieved: "+(data).decode())
 response = input("Reply: ")
 if response == "exit":
     break
 s.sendall(response.encode())
s.close()
