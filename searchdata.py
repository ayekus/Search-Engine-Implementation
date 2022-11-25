import os

global mapping
mapping = {}

def create_mapping():
    read = open(os.path.join('data', 'url_id.txt'), 'r')
    content = read.readlines()
    read.close()
    for line in content:
        num = line[line.rfind('#')+1:]
        num = num.strip()
        url = line[:line.rfind('#')]
        if num != '':
            mapping[url] = int(num)

def get_mapping():
    return mapping

def get_outgoing_links(URL):
    if URL in mapping:
        read = open(os.path.join('data', str(mapping[URL]), 'outgoing_links.txt'), 'r')
        outgoingURLs = read.readlines()
        read.close()
        count = 0
        for url in outgoingURLs:
            outgoingURLs[count] = url.strip()
            count += 1
        return outgoingURLs
    return None

def get_incoming_links(URL):
    if URL in mapping:
        read = open(os.path.join('data', str(mapping[URL]), 'incoming_links.txt'), 'r')
        incomingURLs = read.readlines()
        read.close()
        count = 0
        for url in incomingURLs:
            incomingURLs[count] = url.strip()
            count += 1
        return incomingURLs
    return None

def get_page_rank(URL):
    if URL in mapping:
        read = open(os.path.join('data', str(mapping[URL]), 'pagerank.txt'), 'r')
        pagerank = float(read.readline())
        read.close()
        return pagerank
    return -1

def get_idf(word):
    word = word.strip()
    if os.path.exists(os.path.join('data', 'idf', word + '.txt')):
        read = open(os.path.join('data', 'idf', word + '.txt'), 'r')
        idf = float(read.readline())
        read.close()
        return idf
    return 0

def get_tf(URL, word):
    if URL in mapping and os.path.exists(os.path.join('data', str(mapping[URL]), 'tf', word + '.txt')):
        read = open(os.path.join('data', str(mapping[URL]), 'tf', word + '.txt'), 'r')
        tf = float(read.readline())
        read.close()
        return tf
    return 0

def get_tf_idf(URL, word):
    if URL in mapping and os.path.exists(os.path.join('data', str(mapping[URL]), 'tfidf', word + '.txt')):
        read = open(os.path.join('data', str(mapping[URL]), 'tfidf', word + '.txt'), 'r')
        tfidf = float(read.readline())
        read.close()
        return tfidf
    return 0

def get_title(file):
    read = open(os.path.join('data', file, 'title.txt'), 'r')
    title = read.readline()
    read.close()
    return title
