import socket
 
host = '192.168.218.139'
port = 50010
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print ("Connection from", addr)
while True:
    data = conn.recv(1024)
    if not data: break
    print("Recieved: "+(data).decode())
    response = raw_input("Reply: ")
    if response == "exit":
        break
    conn.sendall(response.encode())
conn.close()
