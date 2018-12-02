MESSAGE_TYPE_SIZE = 4  # Size of message type string.
NUMBER_SIZE = 8  # Size of number string.
TYPE_SIZE = 4  # Size of content type string.
CODE_SIZE = 3  # Size of ack and error codes.

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

    composed = [SEND_URLS_CODE, str(len(urls)).zfill(NUMBER_SIZE)]
    for url, id in zip(urls, ids):
        composed.append(str(len(url)).zfill(NUMBER_SIZE))
        # TODO: check if the ids are strings
        composed.append(str(id).zfill(NUMBER_SIZE))
        composed.append(url)

    return ''.join(composed)


def compose_crawled(main_id, urls, text, content_type):
    '''
    Creates a CRWL message.
    main_id: id of the crawled url.
    urls: list of URLs.
    content_type: content type of the main url.
    text: the text content of the crawled url.
    '''
    # TODO: check if the ids are strings
    composed = [SEND_CRAWLED_DATA_CODE, str(main_id).zfill(NUMBER_SIZE),
                str(len(urls)).zfill(NUMBER_SIZE)]
    for url in urls:
        composed.append(str(len(url)).zfill(NUMBER_SIZE))
        composed.append(url)

    composed.append(str(len(text)).zfill(NUMBER_SIZE))
    composed.append(text)
    composed.append(content_type)

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
    idx = 4
    urls_size = int(message[idx:idx + NUMBER_SIZE])
    idx += NUMBER_SIZE

    urls = []
    ids = []
    for i in range(urls_size):
        url_size = int(message[idx:idx + NUMBER_SIZE])
        idx += NUMBER_SIZE

        id = message[idx:idx + NUMBER_SIZE]
        ids.append(int(id))  # TODO: check if the ids are strings
        idx += NUMBER_SIZE

        url = message[idx:idx + url_size]
        urls.append(url)
        idx += url_size

    return urls, ids


def parse_crawled_message(message):
    '''
    Parses an CRWL message.
    Returns the main ID, a list of urls, the crawled text and content type.
    '''

    idx = 4
    # TODO: check if the ids are strings
    main_id = int(message[idx:idx + NUMBER_SIZE])
    idx += NUMBER_SIZE

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
