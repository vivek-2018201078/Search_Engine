import linecache
import sys
from Stemmer import Stemmer
from nltk.corpus import stopwords
import re
from operator import add
stemmer = Stemmer('english')
stop_words = list(stopwords.words('english'))

doc_map = {}
count_map = {}

def get_counts(text, field):
    counts = [0] * 6
    spl = re.findall(r'\d+', text)
    itr = 0
    if 't' in text:
        if field == 'title' or field == 'all':
            counts[0] = int(spl[itr]) * 100
        itr += 1
    if 'b' in text:
        if field == 'body' or field == 'all':
            counts[1] = int(spl[itr])
        itr += 1
    if 'c' in text:
        if field == 'category' or field == 'all':
            counts[2] = int(spl[itr])
        itr += 1
    if 'i' in text:
        if field == 'infobox' or field == 'all':
            counts[3] = int(spl[itr])
        itr += 1
    if 'e' in text:
        if field == 'external' or field == 'all':
            counts[4] = int(spl[itr])
        itr += 1
    if 'r' in text:
        if field == 'reference' or field == 'all':
            counts[5] = int(spl[itr])
        itr += 1
    return counts

def getline(word, filename, field):
    f = open(filename, "r")
    line = f.readline()
    while line:
        if line.startswith(word):
            #print(line)
            key, index = line.split(':')
            docs = index.split('|')
            for doc in docs:
                doc_no, doc_index = doc.split('-')
                doc_no = doc_no[1:]
                counts = get_counts(doc_index, field)
                if doc_no not in doc_map:
                    doc_map[doc_no] = counts
                else:
                    doc_map[doc_no] = list(map(add,counts, doc_map[doc_no]))

            break
        line = f.readline()

def get_list(q, filename):
    for word in q:
        getline(word, filename, 'all')
    for doc in doc_map.keys():
        count_map[doc] = sum(doc_map[doc])


    list = sorted(count_map.items(), reverse=True, key=lambda x: x[1])
    itr = 0
    for i in list:
        if itr == 10:
            break
        f = open('/home/vivek/PycharmProjects/Search_Engine/index/id_title_map.txt')
        id = str(i[0]) + ':'
        line = f.readline()
        while line:
            if line.startswith(id):
                f, colon, title = line.partition(':')
                title = title[:-1]
                print(title)
                break
            line = f.readline()
        itr += 1




filename = '/home/vivek/PycharmProjects/Search_Engine/index/final.txt'
query = "St. Bartholomew's Church, Ljubljana"
split = re.split(r"[^A-Za-z0-9]+", query)
q = []
for t in split:
    t = stemmer.stemWord(t.lower())
    q.append(t + ':')
print(q)
get_list(q, filename)