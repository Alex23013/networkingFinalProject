import connection as con
from protocol import (AVAILABLE_CODE, SEND_URLS_CODE, SEND_CRAWLED_DATA_CODE,
                      ACKNOWLEDGE_CODE, ERROR_CODE)

import protocol as prt
from threading import Thread
import queue
import socket
import time
from ElasticSearchClient import save, createDict
from serverlogic import getAllUrlsElastic, distributeUrls

general_queue = queue.Queue()
error_queue = queue.Queue()
all_connections = []
all_threads = []
connections_adr = {}

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
            available_threads = False
            for cthread in all_threads:
                if cthread.available:
                    available_threads = True
                    break
            links = []
            if available_threads:
                links = getAllUrlsElastic()
            else:
                time.sleep(2)
                continue
            if len(links) == 0:
                time.sleep(2)
                continue

            av_threads = []
            for cthread in all_threads:
                if cthread.available:
                    av_threads.append(cthread.connection)

            urls_distributed = distributeUrls(links, av_threads)
            for connection in urls_distributed:
                if len(urls_distributed[connection]) == 0:
                    continue
                msgstr = prt.compose_urls([str(link.url) for link in urls_distributed[connection]],
                                          [str(link.id) for link in urls_distributed[connection]])
                con.sendMsg(connection, msgstr)
                print("Sent", len(urls_distributed[connection]), "to", connections_adr[connection])
                for i in all_threads:
                    if i.connection == connection:
                        i.available = False
                        break
            time.sleep(2)


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
        self.available = True

    def run(self):
        message = "cone"
        self.safe_send(message)
        while True:
            msgType, size, data = con.receiveMsg(self.connection)
            print('DATA: ' + data)
            try:
                if data == 'EMPTY!<>!':
                    break
                elif msgType == AVAILABLE_CODE:
                    self.available = True
                # elif msgType == ACKNOWLEDGE_CODE or msgType == ERROR_CODE:
                #     print("Recieved: " + msgType + " code: " + data)
                # elif msgType == SEND_URLS_CODE or msgType == SEND_CRAWLED_DATA_CODE:
                #     print("Recieved: " + msgType + " size: " + size + " content" + data)
                elif data == "exit":
                    print("EXIT!!!!")
                    self.handle_disconnect()
            except socket.error as e:
                print(e.message)

        print('SALE DEL WHILE!!!!!')

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

    def handle_disconnect(self):
        self.connection.close()


conn = con.connectionServer()
ids = 1
actual = 0

ms = DataSender(all_connections, general_queue)
ms.setDaemon(True)
ms.start()


class CommandLineInterface(object):

    def input_command(self, command):
        tokens = self.parse_command(command=command)
        self.process_tokens(tokens=tokens)

    def parse_command(self, command):
        return str(command).split()

    def process_tokens(self, tokens):
        if tokens[0] == "process":
            self.crawl_first_url(tokens[1])

    def crawl_first_url(self, url):
        """Send the url to the crawler"""
        global ids
        save(createDict(url, "", "", False))
        while True:
            connec, addr = conn.accept()
            connections_adr[connec] = addr
            cc = ClientThread(ids + 0, connec, general_queue, all_connections)
            all_threads.append(cc)
            ids += 1
            all_connections.append(cc)
            print("Connection added: ")
            print(addr)
            cc.start()


cli = CommandLineInterface()
while True:
    command = input()
    cli.input_command(command)
