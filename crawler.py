import webdev
import os
import math
import matmult
import searchdata


def crawl(seed):
    fresh_crawl()
    global totalPages
    totalPages = 0
    global queue
    queue = [seed]
    global incoming_links
    incoming_links = {}
    global allWords
    allWords = {}
    global read
    read = []
    while len(queue) > 0:
        content = webdev.read_url(queue[0])
        write_info(content)
        #to get rid of that URL after info is stored and add it to read
        read.append(queue.pop(0))
        totalPages += 1
 
    write_final_info()
    #all files are done - create mapping will be finlized before all searches happen
    return totalPages 

#removes all past crawl data 
def fresh_crawl():
    dataDir = 'data'
    if os.path.isdir(dataDir) is False:
        os.makedirs(dataDir)
        fileout = open(os.path.join('data', 'url_id.txt'), "w")
        fileout.close()
        return
    data = os.listdir(dataDir)
    for files in data:
        if os.path.isdir(os.path.join(dataDir, files)):
            data2 = os.listdir(os.path.join(dataDir, files))
            for file2 in data2:
                if os.path.isdir(os.path.join(dataDir, files, file2)):
                    data3 = os.listdir(os.path.join(dataDir, files, file2))
                    for file3 in data3:
                        os.remove(os.path.join(dataDir, files, file2, file3))
                    os.rmdir(os.path.join(dataDir, files, file2))
                else:
                    os.remove(os.path.join(dataDir, files, file2))
            os.rmdir(os.path.join(dataDir, files))
        else:
            os.remove(os.path.join(dataDir, files))



#creates most of the files and folders for new crawled data
def write_info(content):
    os.makedirs(os.path.join('data', str(totalPages)))

    #to get and save page title
    fileout = open(os.path.join('data', str(totalPages), 'title.txt'), "w")
    title = content[(content.find('<title>') + 7):content.find('</title>')]
    fileout.write(title)
    fileout.close()
    
    #for all of tf and creating files for tfidf
    os.makedirs(os.path.join('data', str(totalPages), 'tf'))
    os.makedirs(os.path.join('data', str(totalPages), 'tfidf'))

    #for getting all the information from the page
    words = {}
    totalWords = 0
    tempContent = content
    last = content

    #repeat until there aren't anymore p tags
    while True:
        tempContent = tempContent[(tempContent.find('<p')):]
        #if it doesn't find another instance of <p, it will be the same as the last tempContent - therefour stopping the loop
        if tempContent == last:
            break;
        info = tempContent[(tempContent.find('>')+1):tempContent.find('</p>')]
        if '\n' in info:
            info = info.split('\n')
        else:
            info = info.split(' ')
        for word in info:
            if word != '':
                if word not in words:
                    words[word] = 1.0
                    totalWords += 1.0
                else:
                    words[word] += 1.0
                    totalWords += 1.0
        #this is to get rid of the instance of <p to make sure that in the next loop it doesn't go through the same paragraph
        tempContent[1:]
        last = tempContent

    for word in words:
        fileout = open(os.path.join('data', str(totalPages), 'tf', word + '.txt'), "w")
        fileout.write(str(words[word]/totalWords))
        fileout.close()
        fileout = open(os.path.join('data', str(totalPages), 'tfidf', word + '.txt'), "w")
        fileout.close()

        #add words to allWords for idf
        if word in allWords:
            allWords[word] += 1
        else:
            allWords[word] = 1

    #for incoming and outgoing links and adding new links to queue
    links_out = []
    content = content.split('\n')
    for line in content:
        if 'href' in line:
            line = line[(line.find('href="'))+6:line.find('">')]
            if 'http://' not in line:
                if './' in line:
                    line = line[line.find('./')+2:]
                    line = queue[0][:queue[0].rfind('/')+1] + line
            links_out.append(line)
            if line not in read and line not in queue:
                queue.append(line)

    #writing outgoing links
    fileout = open(os.path.join('data', str(totalPages), 'outgoing_links.txt'), "w")
    for link in links_out:
        fileout.write(link + '\n')
    fileout.close()

    if os.path.exists(os.path.join('data', 'url_id.txt')):
        write = open(os.path.join('data', 'url_id.txt'), "a")
        write.write('\n' + queue[0] + '#' + str(totalPages))
        write.close()
    else:
        write = open(os.path.join('data', 'url_id.txt'), "w")
        write.write(queue[0] + '#' + str(totalPages))
        write.close()

    #storing info for incoming links
    for link in links_out:
        #if this link already has other URLs leading to it then it will add it to that list
        if link in incoming_links:
            incoming_links[link].append(queue[0])
        else:
            incoming_links[link] = [queue[0]]

def write_final_info():
    #create and get mapping
    searchdata.create_mapping()
    mapping = searchdata.get_mapping()

    #write incoming links
    for key in incoming_links:
        fileout = open(os.path.join('data', str(mapping[key]), 'incoming_links.txt'), 'w')
        for link in incoming_links[key]:
            fileout.write(link + '\n')
        fileout.close()

    #write idf
    os.makedirs(os.path.join('data', 'idf'))
    for word in allWords:
        fileout = open(os.path.join('data', 'idf', word+'.txt'), "w")
        fileout.write(str(math.log((totalPages/(1+allWords[word])), 2)))
        fileout.close()

    #write tfidf
    for i in range(0, totalPages):
        files = os.listdir(os.path.join('data', str(i), 'tfidf'))
        for file in files:
            add = open(os.path.join('data', str(i), 'tfidf', file), "a")
            readtf = open(os.path.join('data', str(i), 'tf', file), "r")
            readidf = open(os.path.join('data', 'idf', file), "r")
            tf = float(readtf.readline())
            idf = float(readidf.readline())
            add.write(str((math.log(1+tf,2))*idf))
            readidf.close()
            add.close()
            readtf.close()
    
    #write page ranks
    matrix = []
    alpha = 0.1
    for i in range(0, totalPages):
        read = open(os.path.join('data', str(i), 'outgoing_links.txt'), "r")
        content = read.readlines()
        read.close()
        temp = [0] * totalPages
        for line in content:
            adjacency = (1/len(content))
            line = line.strip()
            temp[mapping[line]] = ((1-alpha) * adjacency)
        
        for num in range(0, len(temp)):
            temp[num] += alpha/totalPages
        matrix.append(temp)
    
    old = [[(1/totalPages)] * totalPages]

    while True:
        new = (matmult.mult_matrix(old, matrix))
        if (matmult.euclidean_dist(new, old)) < 0.0001:
            break;
        old = new

    folder = 0
    for num in new[0]:
        fileout = open(os.path.join('data', str(folder), 'pagerank.txt'), "w")
        fileout.write(str(num))
        folder += 1
        fileout.close()
