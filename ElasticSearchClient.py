from elasticsearch_dsl import Document, Search, connections, Text, Boolean

# name of index(like table)
IP_PORT_SERVER = '192.168.197.251:9200'
INDEX = 'pepito54'

connections.create_connection(timeout=60)

connections.configure(
    default={
        'hosts': IP_PORT_SERVER,
    }
)

client = connections.get_connection()

class Link(Document):
    url = Text()
    text = Text()
    type = Text()
    crawled = Boolean()

    class Index:
        name = INDEX


def save(dataDict):
    if not Link._index.exists():
        Link.init()

    newlink = Link()

    # setting data
    # newlink.meta.id = dataDict['id']
    newlink.url = dataDict['url']
    newlink.text = dataDict['text']
    newlink.type = dataDict['type']
    newlink.crawled = dataDict['crawled']

    # saving in index(like a table)
    newlink.save()


def listAll():
    s = Search(using=client, index=INDEX)
    results = s.execute()

    for link in results:
        # print (link)
        print(link.meta.id, link.url, link.type)

def listAllDontCrawled():
    linkscrawledList = []
    try:
        s = Search(using=client, index=INDEX).filter("term", crawled=False)
        count = s.count()
        results = s[0:count].execute()

        for link in results:
            print(link.meta.id, link.url, link.type, link.crawled)
            auxlink = Link()
            auxlink.id = link.meta.id
            auxlink.url = link.url
            auxlink.type = link.type
            auxlink.crawled = link.crawled
            auxlink.text = link.text

            linkscrawledList.append(auxlink)

        return linkscrawledList
    except:
        return linkscrawledList


def getAliases():
    conn = client.indices.get_alias().keys()
    print(conn)


def searchByIndex(index):
    try:
        searched = Link.get(index)
        if searched:
            return searched
    except:
        return False


def createDict(url, text, type, crawled=False):
    newdict = {
        'url': url,
        'type': text,
        'text': type,
        'crawled': crawled
    }
    return newdict


def updateAllFields(index, fieldDict):
    searched = searchByIndex(index)
    if not searched:
        print("ERROR: Index dont exist ", index)
        return
    # setting data
    # searched.meta.id = fieldDict['id']
    # searched.url = fieldDict['url']
    searched.text = fieldDict['text']
    searched.type = fieldDict['type']
    searched.crawled = fieldDict['crawled']

    # saving in index(like a table)
    searched.save()


if __name__ == '__main__':
    # new = {
    #     'url': "www.id1.com",
    #     'type': "link2",
    #     'text': "tercertest",
    #     'crawled': False
    #     #'id': 1
    # }

    # save(new)
    # listAllDontCrawled()
    #print("----------------")
    listAllDontCrawled()

    #getAliases()
    '''
    new = {
        'url': "www.asdfasdf.com",
        'type': "link2222",
        'text': "holahola222",
    }

    updateAllFields(1, new)
    listAll()
    # getAliases()
    # print( searchByIndex(2) )
    '''
