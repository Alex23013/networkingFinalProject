import connection as con
from protocol import (AVAILABLE_CODE, SEND_URLS_CODE, SEND_CRAWLED_DATA_CODE,
                      ACKNOWLEDGE_CODE, ERROR_CODE) 

from threading import Thread
import queue

general_queue = queue.Queue()
error_queue = queue.Queue()
all_connections = []

class DataSender(Thread):
    """ This class handles the connections where to send a message """

    def __init__(self, clients, queue):
        Thread.__init__(self)
        self.list_of_clients = clients
        self.queue_messages = queue

    def run(self):
        """
        Here we handle the messages that are in the queue of messages
        Messages Structure: Tuple (message, client id)
        """
        while True:
            message = self.queue_messages.get()
            if message is None or message is '':
                continue

            if message[0].__class__.__name__ != 'str':
                print ('Sending some not str message')

            self.send_to_id(message[0], message[1])

    def send_to_id(self, message , id_connection):
        print ('SENDING '+ message+ ' TO'+ id_connection)
        for client in self.list_of_clients:
            if client.get_id() == id_connection:
                try:
                    con.sendMsg (client.connection,message)    
                except socket.error:
                    error_queue.put('cannot send value to client with id = ' + str(client.get_id()))
                break

 
class ClientThread(Thread):
    """ This class handle the client connection, data, etc. ; in a thread """

    def __init__(self, assigned_id, connection, message_queue, list_connected):
        Thread.__init__(self)
        self.queue = message_queue
        self.connection = connection
        self.list_of_connected = list_connected
        self.client_data = {
            'id': assigned_id,
        }
    
    def safe_send(self, message):
        general_queue.put((message, self.client_data['id']))

    def get_id(self):
        return self.client_data['id']

    def safe_recv(self):
        try:
            msgType, size, data = con.receiveMsg(self.connection)
            return msgType, size, data
        except socket.error:
            error_queue.put('cannot receive data from client with id = ' + str(self.client_data['id']))
            return None

conn = con.connectionServer()
sock, addr = conn.accept()
print ("Connection from", addr)
  
ids = 1
actual = 0

ms = DataSender(all_connections, general_queue)
ms.setDaemon(True)
ms.start()


while True:
  connec, addr = conn.accept()
  cc = ClientThread(ids + 0, connec, general_queue, all_connections)
  ids += 1
  all_connections.append(cc)
  print ("Connection added: ")
  print( addr)
  cc.start()
  '''msgType, size, data = con.receiveMsg(sock)
  if data == '': break
  if msgType == AVAILABLE_CODE:
    print("Recieved: "+msgType)
  if msgType == ACKNOWLEDGE_CODE or msgType == ERROR_CODE:
    print("Recieved: "+msgType+ "code: "+data)
  if msgType == SEND_URLS_CODE or msgType == SEND_CRAWLED_DATA_CODE:
    print("Recieved: "+msgType+ "size: "+ size + "content"+data)
   
  response = input("Reply: ")
  con.sendMsg (sock,response)    
  if response == "exit":
    break''' 
sock.close()

