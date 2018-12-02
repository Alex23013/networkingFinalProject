from multiprocessing import Pool
import crawler as crw 
import protocol as pro 

CNT_TYPE_TEXT = 'text'

def process_url(url_id):
    '''
    Receives a tuple of url and id.
    Returns a message with the crawled data.
    '''
    url, id = url_id
    content_type = crw.extract_content_type(url)
    text = ''
    links = []
    if content_type == CNT_TYPE_TEXT:
        text, links = crw.extract_text_links(url)
    return pro.compose_crawled(id, links, text, content_type)


if __name__ == '__main__':
    # Connect with master
    # ...

    message = pro.compose_available()
    # Send message to master
    # ...
    while (True):
        # Receive URLS
        # TODO: check if the receive network block the process until it receives a message.
        message  # = receive_message
        urls, ids  = pro.parse_urls_message(message)

        with Pool() as pool:
            messages = pool.map(process_url, zip(urls, ids))
            # Send messages to master
        
        message = pro.compose_available()
        # Send message to master
        # ...
        # Sleep?
            

