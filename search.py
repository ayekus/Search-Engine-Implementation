import os
import math
import searchdata


def search(phrase, boost):
    top10 = []
    files = os.listdir('data')
    allFiles = []
    files.remove('idf')
    files.remove('url_id.txt')

    phrase = phrase.lower()
    search = phrase.split()
    
    numWords = 0
    words = {}
    for word in search:
        numWords += 1
        if word in words:
            words[word] += 1
        else:
            words[word] = 1

    #query order is to remember the order for queryVectors of each site
    queryOrder = []
    queryVector = []
    toDelete = []
    #to get the query vector numbers and to remember the specific way in which they are ordered
    for word in words:
        if not os.path.isfile(os.path.join('data', 'idf', word + '.txt')):
            #meaning there is no site with listed word on it
            toDelete.append(word)
        else:
            idf = searchdata.get_idf(word)
            queryOrder.append(word)
            queryVector.append((math.log(1+(words[word]/numWords)))*idf)

    #for deleting any words that are never mentioned in the whole crawl
    for word in toDelete:
        del words[word]

    #because the left denominator in the cosine similarity is always constant
    denomLeft = 0
    for num in queryVector:
        denomLeft += num**2
    denomLeft = math.sqrt(denomLeft)

    #to get links in O(1) time for each page
    reverseMapping = {}
    read = open(os.path.join('data', 'url_id.txt'), 'r')
    content = read.readlines()
    read.close()
    for line in content:
        num = line[line.rfind('#')+1:]
        num = num.strip()
        url = line[:line.rfind('#')]
        reverseMapping[num] = url

    #to get each sites score, title and url
    for file in files:
        add = {}
        #get title
        add['title'] = searchdata.get_title(file)

        #get url from reverse mapping dictionary:
        add['url'] = reverseMapping[file]

        #to calculate the cosine similarity (score) for the site
        #get tfidf at each word in the correct order
        docVector = []
        for word in queryOrder:
            docVector.append(searchdata.get_tf_idf(reverseMapping[file], word))

        denomRight = 0
        numerator = 0
        for i in range(0, len(queryVector)):
            numerator += queryVector[i]*docVector[i]
            denomRight += docVector[i]**2
        if denomRight == 0:
            cosineSimilarity = 0
        else:
            denomRight = math.sqrt(denomRight)
            cosineSimilarity = numerator/(denomLeft*denomRight)
        
        #if boost is True then we want to multiply page rank by the cosine similarity value  to give us final score
        if boost:
            pagerank = searchdata.get_page_rank(reverseMapping[file])
            add['score'] = cosineSimilarity * pagerank
        else:
            add['score'] = cosineSimilarity
        allFiles.append(add)

    #to get the top 10 highest values using a kind of selection sort
    for _ in range(10):
        biggest = 0
        index = -1
        for j in range(len(allFiles)):
            if allFiles[j]["score"] >= biggest:
                biggest = allFiles[j]["score"];
                index = j
        top10.append(allFiles[index])
        allFiles.pop(index)
    return top10