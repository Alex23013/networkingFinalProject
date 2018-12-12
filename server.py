import connection as con
 
sock = con.connection("server")

while True:
    data = con.receiveMsg(sock, 1024)
    if data == None: break
    print("Recieved: "+data)
    
    response = input("Reply: ")
    con.sendMsg (sock,response)    
    if response == "exit":
        break
sock.close()
