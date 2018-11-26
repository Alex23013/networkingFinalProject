NUMBER_CHARS = 4

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

    composed = [SEND_CRAWLED_DATA_CODE, str(main_id).zfill(NUMBER_CHARS),
                str(len(urls).zfill(NUMBER_CHARS))]
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


def fragment_message(message, chunk_size):
    ''' Fragments a message. '''
    chunks = []

    for i in range(0, len(message), chunk_size):
        chunks.append(message[i:i + chunk_size])

    return chunks
