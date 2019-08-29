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
            counts[0] = int(spl[itr]) * 200
        itr += 1
    if 'b' in text:
        if field == 'body' or field == 'all':
            counts[1] = int(spl[itr])
        itr += 1
    if 'c' in text:
        if field == 'category' or field == 'all':
            counts[2] = int(spl[itr]) * 20
        itr += 1
    if 'i' in text:
        if field == 'infobox' or field == 'all':
            counts[3] = int(spl[itr]) * 40
        itr += 1
    if 'e' in text:
        if field == 'ext' or field == 'all':
            counts[4] = int(spl[itr]) * 15
        itr += 1
    if 'r' in text:
        if field == 'ref' or field == 'all':
            counts[5] = int(spl[itr]) * 10
        itr += 1
    return counts

def getline(word, field, filename):
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
    for word, field in q:
        getline(word, field, filename)
    for doc in doc_map.keys():
        count_map[doc] = sum(doc_map[doc])


    list = sorted(count_map.items(), reverse=True, key=lambda x: x[1])
    itr = 0
    for i in list:
        if itr == 10:
            break
        f = open('/home/vivek/PycharmProjects/Search_Engine/index/id_title_map.txt')
        id = str(i[0]) + ':'
        if i[1] == 0:
            break
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
query = "body:pierfit"
field = ['title:', 'body:', 'category:', 'infobox:', 'external:', 'ref:']
q = []
if any(f in query for f in field):
    temp = re.split(':', query)
    field = 'all'
    for t in temp:
        words = t.split()
        for i in range(len(words)):
            if i == len(words) - 1 and words[i] == 'title':
                field = 'title'
            elif i == len(words) - 1 and words[i] == 'body':
                field = 'body'
            elif i == len(words) - 1 and words[i] == 'category':
                field = 'category'
            elif i == len(words) - 1 and words[i] == 'infobox':
                field = 'infobox'
            elif i == len(words) - 1 and words[i] == 'ext':
                field = 'ext'
            elif i == len(words) - 1 and words[i] == 'ref':
                field = 'ref'
            else:
                x = stemmer.stemWord(words[i].lower())
                q.append((x + ':', field))
else:
    split = re.split(r"[^A-Za-z0-9]+", query)
    q = []
    for t in split:
        t = stemmer.stemWord(t.lower())
        q.append((t + ':', 'all'))
get_list(q, filename)