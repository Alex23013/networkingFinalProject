import socket
from protocol import (NUMBER_SIZE, TYPE_SIZE, CODE_SIZE,
                      AVAILABLE_CODE, SEND_URLS_CODE, SEND_CRAWLED_DATA_CODE,
                      ACKNOWLEDGE_CODE, ERROR_CODE)

import protocol as prt

host = '192.168.167.8'
port = 50018  
chunk_size = 1024

def receiveMsg (sock):
  msgType = sock.recv(TYPE_SIZE)
  msgType = msgType.decode()  
  if msgType == AVAILABLE_CODE:
    return msgType, None , None 

  if msgType == ACKNOWLEDGE_CODE or msgType == ERROR_CODE:
    data =  sock.recv(CODE_SIZE)
    return msgType, '', data.decode()  

  if msgType == SEND_URLS_CODE or msgType == SEND_CRAWLED_DATA_CODE:
    size = sock.recv(NUMBER_SIZE)
    sizeInt = int(size.decode())
    data = sock.recv(sizeInt)   
    return msgType, size.decode(), data.decode() 
    
  if msgType == "exit": return '', '', ''
  
def sendMsg (sock,response):
  if len(response) > chunk_size :
    fragments = prt.fragment_message(response, chunk_size )
    for i in range(len(fragments)):
      sock.sendall(fragments[i].encode())
  else :  
    sock.sendall(response.encode())

def connectionClient ():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
  sock.connect((host, port))
  print("Connected to "+(host)+" on port "+str(port))
  return sock
  
def connectionServer() :
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
  try:
    sock.bind((host, port))
    
  except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
	
  print('Socket bind complete')

  sock.listen(5)
  print ('Socket now listening')
  return sock

  

    
  

