import connection as con
 
s = con.connection("client")
initialMessage = input("Send: ")
con.sendMsg (s,initialMessage)
 
while True:
  data = con.receiveMsg(s, 1024)
  if data == None: break
  print("Recieved: "+data)

  response = input("Reply: ")
  con.sendMsg (s,response)  
  if response == "exit":
     break
print("programFinished")
