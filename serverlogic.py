from ElasticSearchClient import listAllDontCrawled
from elasticsearch_dsl import Document, Search, connections, Text


def getAllUrlsElastic():
    """Provisional method, must be implemented in ElasticSearchClient"""
    return listAllDontCrawled()

def distributeUrls(urls, clients):
    lenurls = len(urls)
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
