NUMBER_CHARS = 4
TYPE_CHARS = 4

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

    composed = [SEND_URLS_CODE, str(len(urls)).zfill(NUMBER_CHARS)]
    for url, id in zip(urls, ids):
        composed.append(str(len(url)).zfill(NUMBER_CHARS))
        # TODO: check if the ids are strings
        composed.append(str(id).zfill(NUMBER_CHARS))
        composed.append(url)

    return ''.join(composed)


def compose_crawled(main_id, urls, types, text):
    '''
    Creates a CRWL message.
    main_id: id of the crawled url.
    urls: list of URLs.
    types: list of types, must have the same size of the URLs list.
    text: the text content of the crawled url.
    '''

    if (len(urls) != len(types)):
        print("ERROR: URL list and Types list must have the same size.")
        return ''

    # TODO: check if the ids are strings
    composed = [SEND_CRAWLED_DATA_CODE, str(main_id).zfill(NUMBER_CHARS),
                str(len(urls)).zfill(NUMBER_CHARS)]
    for url, _type in zip(urls, types):
        composed.append(str(len(url)).zfill(NUMBER_CHARS))
        composed.append(url)
        composed.append(_type)

    composed.append(str(len(text)).zfill(NUMBER_CHARS))
    composed.append(text)

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
    urls_size = int(message[idx:idx + NUMBER_CHARS])
    idx += NUMBER_CHARS

    urls = []
    ids = []
    for i in range(urls_size):
        url_size = int(message[idx:idx + NUMBER_CHARS])
        idx += NUMBER_CHARS

        id = message[idx:idx + NUMBER_CHARS]
        ids.append(int(id))  # TODO: check if the ids are strings
        idx += NUMBER_CHARS

        url = message[idx:idx + url_size]
        urls.append(url)
        idx += url_size

    return urls, ids


def parse_crawled_data_message(message):
    '''
    Parses an CRWL message.
    Returns the main ID, a list of urls and the crawled text
    '''

    idx = 4
    # TODO: check if the ids are strings
    main_id = int(message[idx:idx + NUMBER_CHARS])
    idx += NUMBER_CHARS

    urls_size = int(message[idx:idx + NUMBER_CHARS])
    idx += NUMBER_CHARS

    urls = []
    types = []

    for i in range(urls_size):
        url_size = int(message[idx:idx + NUMBER_CHARS])
        idx += NUMBER_CHARS

        url = message[idx:idx + url_size]
        urls.append(url)
        idx += url_size

        _type = message[idx:idx + TYPE_CHARS]
        types.append(_type)
        idx += TYPE_CHARS

    text_size = int(message[idx:idx + NUMBER_CHARS])
    idx += NUMBER_CHARS

    text = message[idx:idx + text_size]

    return main_id, urls, text


def fragment_message(message, chunk_size):
    ''' 
    Fragments a message.
    Returns a list with the fragmented message.
    '''
    chunks = []

    for i in range(0, len(message), chunk_size):
        chunks.append(message[i:i + chunk_size])

    return chunks

# URLS 0004
# 0008 0010 pepe.com
# 0008 0011 papa.com
# 0009 0012 comida.pe
# 0010 0013 hambre.asd
