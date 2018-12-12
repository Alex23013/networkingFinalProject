MESSAGE_TYPE_SIZE = 4  # Size of message type string.
NUMBER_SIZE = 8  # Size of number string.
TYPE_SIZE = 4  # Size of content type string.
CODE_SIZE = 3  # Size of ack and error codes.
ID_SIZE = 20

AVAILABLE_CODE = 'AVLB'
SEND_URLS_CODE = 'URLS'
SEND_CRAWLED_DATA_CODE = 'CRWL'
ACKNOWLEDGE_CODE = 'ACKN'
ERROR_CODE = 'ERRO'


def compose_available():
    '''
    Creates an AVLB message.
    '''
    return AVAILABLE_CODE


def compose_urls(urls, ids):
    '''
    Creates an URLS message.
    - urls: list of URLs.
    - ids: list of IDs, must have the same size of the URLs list.
    '''

    if (len(urls) != len(ids)):
        print("ERROR: URL list and ID list must have the same size.")
        return ''

    composed = [SEND_URLS_CODE]
    content = [str(len(urls)).zfill(NUMBER_SIZE)]
    for url, id in zip(urls, ids):
        if (not isinstance(id, str) or len(id) != ID_SIZE):
            print("ERROR: The Id size isn't 20")
            return ''
        content.append(str(len(url)).zfill(NUMBER_SIZE))
        # TODO: check if the ids are strings
        content.append(id)
        content.append(url)

    content_str = ''.join(content)
    composed.append(str(len(content_str)).zfill(NUMBER_SIZE))
    composed.append(content_str)

    return ''.join(composed)


def compose_crawled(main_id, urls, text, content_type):
    '''
    Creates a CRWL message.
    main_id: id of the crawled url.
    urls: list of URLs.
    content_type: content type of the main url.
    text: the text content of the crawled url.
    '''

    if (not isinstance(main_id, str) or len(main_id) != ID_SIZE):
        print("ERROR: The Id size isn't 20")
        return ''

    # TODO: check if the ids are strings
    composed = [SEND_CRAWLED_DATA_CODE]
    content = [main_id,
               str(len(urls)).zfill(NUMBER_SIZE)]
    for url in urls:
        content.append(str(len(url)).zfill(NUMBER_SIZE))
        content.append(url)

    content.append(str(len(text)).zfill(NUMBER_SIZE))
    content.append(text)
    content.append(content_type)

    content_str = ''.join(content)
    composed.append(str(len(content_str)).zfill(NUMBER_SIZE))
    composed.append(content_str)

    return ''.join(composed)


def compose_ack(code):
    '''
    Creates an ACKN message.
    code: acknowledge code.
    '''
    composed = [ACKNOWLEDGE_CODE, str(code)]
    return ''.join(composed)


def compose_err(code):
    '''
    Creates an ERRO message.
    code: error code.
    '''
    composed = [ERROR_CODE, str(code)]
    return ''.join(composed)


def parse_urls_message(message):
    '''
    Parses an URLS message.
    Returns a list of URLs and a list IDs
    '''
    idx = MESSAGE_TYPE_SIZE + NUMBER_SIZE # ignoring type and content size

    urls_size = int(message[idx:idx + NUMBER_SIZE])
    idx += NUMBER_SIZE

    urls = []
    ids = []
    for i in range(urls_size):
        url_size = int(message[idx:idx + NUMBER_SIZE])
        idx += NUMBER_SIZE

        id = message[idx:idx + ID_SIZE]
        ids.append(id)  # TODO: check if the ids are strings
        idx += ID_SIZE

        url = message[idx:idx + url_size]
        urls.append(url)
        idx += url_size

    return urls, ids


def parse_crawled_message(message):
    '''
    Parses an CRWL message.
    Returns the main ID, a list of urls, the crawled text and content type.
    '''

    idx = MESSAGE_TYPE_SIZE + NUMBER_SIZE # ignoring type and content size
    # TODO: check if the ids are strings
    main_id = message[idx:idx + ID_SIZE]
    idx += ID_SIZE

    urls_size = int(message[idx:idx + NUMBER_SIZE])
    idx += NUMBER_SIZE

    urls = []

    for i in range(urls_size):
        url_size = int(message[idx:idx + NUMBER_SIZE])
        idx += NUMBER_SIZE

        url = message[idx:idx + url_size]
        urls.append(url)
        idx += url_size

    text_size = int(message[idx:idx + NUMBER_SIZE])
    idx += NUMBER_SIZE

    text = message[idx:idx + text_size]
    idx += text_size
    content_type = message[idx: idx + TYPE_SIZE]

    return main_id, urls, text, content_type


def parse_ack_message(message):
    ''' Returns the ack code. '''
    idx = 4
    return message[idx: idx + CODE_SIZE]


def parse_err_message(message):
    ''' Returns the error code. '''
    idx = 4
    return message[idx: idx + CODE_SIZE]


def extract_type(message):
    ''' Returns the message type. '''
    return message[:MESSAGE_TYPE_SIZE]


def fragment_message(message, chunk_size):
    ''' 
    Fragments a message.
    Returns a list with the fragmented message.
    '''
    chunks = []

    for i in range(0, len(message), chunk_size):
        chunks.append(message[i:i + chunk_size])

    return chunks