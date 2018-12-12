from ElasticSearchClient import client, INDEX
from elasticsearch_dsl import Document, Search, connections, Text


def getAllUrlsElastic():
    """Provisional method, must be implemented in ElasticSearchClient"""
    s = Search(using=client, index=INDEX)
    results = s.execute()
    return results


def getAllConnectedClients():
    """ Return all connected clients """
    return [1, 2, 3]


def distributeUrls():
    urls = getAllUrlsElastic()
    lenurls = len(urls)
    clients = getAllConnectedClients()
    lenclients = len(clients)
    num = lenurls // lenclients
    if lenurls % lenclients != 0:
        num += 1
    i = 0
    j = 0
    dicturls = {}
    while i < lenurls:
        minimo = int(min(i + num, lenurls))
        print(i, j, minimo)
        dicturls[clients[j]] = urls[i:minimo]
        print('end ', minimo)
        i += num
        j += 1

    return dicturls


print(distributeUrls())
