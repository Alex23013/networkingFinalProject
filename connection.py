import socket
from protocol import (NUMBER_SIZE, TYPE_SIZE, CODE_SIZE,
                      AVAILABLE_CODE, SEND_URLS_CODE, SEND_CRAWLED_DATA_CODE,
                      ACKNOWLEDGE_CODE, ERROR_CODE)

import protocol as prt
import sys

host = '192.168.197.162'
hostserver = "0.0.0.0"
port = 50003
chunk_size = 1024


def receiveMsg(sock):
    msgType = sock.recv(TYPE_SIZE)
    msgType = msgType.decode()
    print('Tipo de mensaje', msgType)
    if msgType == AVAILABLE_CODE:
        return msgType, '', ''

    if msgType == ACKNOWLEDGE_CODE or msgType == ERROR_CODE:
        data = sock.recv(CODE_SIZE)
        return msgType, '', data.decode()

    if msgType == SEND_URLS_CODE or msgType == SEND_CRAWLED_DATA_CODE:
        size = sock.recv(NUMBER_SIZE)
        sizeInt = int(size.decode())
        data = sock.recv(sizeInt)
        return msgType, size.decode(), data.decode()
    if msgType == "cone":
        return '', '', "1"
    if msgType == "exit":
        return '', '', ''

    return 'ninguno','ninguno','ninguno'



def sendMsg(sock, response):
    if len(response) > chunk_size:
        fragments = prt.fragment_message(response, chunk_size)
        for i in range(len(fragments)):
            sock.sendall(fragments.encode())
    else:
        print("rspo: ", response)
        sock.sendall(response.encode())


def connectionClient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to " + (host) + " on port " + str(port))
    return sock


def connectionServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((hostserver, port))

    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    print('Socket bind complete')

    sock.listen(5)
    print('Socket now listening')
    return sock
