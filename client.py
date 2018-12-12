import connection as con
from protocol import (AVAILABLE_CODE, SEND_URLS_CODE, SEND_CRAWLED_DATA_CODE,
                      ACKNOWLEDGE_CODE, ERROR_CODE) 

s = con.connectionClient()
initialMessage = input("Send: ")
con.sendMsg (s,initialMessage)
 
while True:
  msgType, size, data = con.receiveMsg(s)
  if data == '': break
  if msgType == AVAILABLE_CODE:
    print("Recieved: "+msgType)
  if msgType == ACKNOWLEDGE_CODE or msgType == ERROR_CODE:
    print("Recieved: "+msgType+ "code: "+data)
  if msgType == SEND_URLS_CODE or msgType == SEND_CRAWLED_DATA_CODE:
    print("Recieved: "+msgType+ "size: "+ size + "content"+data)

  response = input("Reply: ")
  con.sendMsg (s,response)  
  if response == "exit":
     break
print("programFinished")
