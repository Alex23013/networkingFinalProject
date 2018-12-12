from multiprocessing import Pool
import crawler as crw 
import protocol as pro 
import ElasticSearchClient as es
import connection as con

CNT_TYPE_TEXT = 'html'

def process_url(url_id):
    '''
    Receives a tuple of url and id.
    Returns a message with the crawled data.
    '''

    url, id = url_id
    print("C> CRAWLING: ", url)
    content_type = crw.extract_content_type(url)
    text = ''
    links = []
    if content_type == CNT_TYPE_TEXT:
        text, links = crw.extract_text_links(url)

    print("C>   Type: ", content_type)
    # print("C>   Link size: ", len(links))
    links_dicts = [es.createDict(i,'','') for i in links]
    update_dict = es.createDict('', text, content_type, True)

    try:
        for i in links_dicts:
            es.save(i)
        es.updateAllFields(id, update_dict)
    except:
        print("C>   ERROR: something gone wrong with: ", url)
    print("C>   DONE: crawled without any problems")

if __name__ == '__main__':
    # Connect with master
    socket = con.connectionClient()

    # Send message to master
    message = pro.compose_available()
    con.sendMsg(socket, message)

    while (True):
        # Receive URLS
        # TODO: check if the receive network block the process until it receives a message.
        mtype, size, content = con.receiveMsg(socket)
        # print(f"> MSG type: {mtype}, Content size: {content} \n Len: {len(content)}")
        message  = ''.join([mtype, size, content]) 
        urls, ids  = pro.parse_urls_message(message)
        # print(f" >> URLS & IDS: {urls} \n {ids}")
        # with Pool() as pool:
            # pool.map(process_url, zip(urls, ids))
        for u, i in zip(urls, ids):
            process_url((u, i))
        
        # Send message to master
        message = pro.compose_available()
        con.sendMsg(socket, message)
        print("> AVLB")

