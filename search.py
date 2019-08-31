import sys
from Stemmer import Stemmer
from nltk.corpus import stopwords
import re
from operator import add
import os

stemmer = Stemmer('english')
stopwords_list = []
stop_words = set()

try:
    with open("stopwords.txt") as input_file:
        for input_line_raw in input_file:
            input_tokens = input_line_raw.split(', ')
            stopwords_list.extend(input_tokens)
            input_tokens = list(map(stemmer.stemWord, input_tokens))
        stop_words = set(stopwords_list)
except:
    stop_words = set(stopwords.words('english'))

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

def get_list(q, final_index_path, title_path):
    for word, field in q:
        getline(word, field, final_index_path)
    for doc in doc_map.keys():
        count_map[doc] = sum(doc_map[doc])


    list = sorted(count_map.items(), reverse=True, key=lambda x: x[1])
    itr = 0
    ans = []
    for i in list:
        if itr == 10:
            break
        f = open(title_path)
        id = str(i[0]) + ':'
        #print(i[1])
        line = f.readline()
        while line:
            if line.startswith(id):
                f, colon, title = line.partition(':')
                title = title[:-1]
                #print(title)
                ans.append(title)
                break
            line = f.readline()
        itr += 1
    return ans
def search_query(query, final_index_path, title_path):
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
                    if x not in stop_words:
                        q.append((x + ':', field))
    else:
        split = re.split(r"[^A-Za-z0-9]+", query)
        q = []
        for t in split:
            t = stemmer.stemWord(t.lower())
            if t not in stop_words:
                q.append((t + ':', 'all'))
    return get_list(q, final_index_path, title_path)

def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')


def search(path_to_index, queries):
    final_index_path = os.path.join(path_to_index, 'final.txt')
    title_path = os.path.join(path_to_index, 'id_title_map.txt')
    output = []
    for query in queries:
        temp = search_query(query, final_index_path, title_path)
        output.append(temp)
        doc_map.clear()
        count_map.clear()
    return output

def main():
    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)
    print("Done. Output at:", path_to_output)

if __name__ == '__main__':
    main()