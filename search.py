import sys
from Stemmer import Stemmer
import re
from operator import add
import os
import timeit
import math
#import linecache

stemmer = Stemmer('english')
stopwords_list = []
stop_words = set()

total_docs = 19567269


with open("stopwords.txt") as input_file:
    for input_line_raw in input_file:
        input_tokens = input_line_raw.split(', ')
        stopwords_list.extend(input_tokens)
        input_tokens = list(map(stemmer.stemWord, input_tokens))
    stop_words = set(input_tokens)
doc_map = {}
def get_counts(text, field):
    counts = [0] * 6
    spl = re.findall(r'\d+', text)
    itr = 0
    if 't' in text:
        if field == 'title' or field == 'all':
            counts[0] = min(1, int(spl[itr])) * 300
        itr += 1
    if 'b' in text:
        if field == 'body' or field == 'all':
            counts[1] = min(int(spl[itr]), 100)
        itr += 1
    if 'c' in text:
        if field == 'category' or field == 'all':
            counts[2] = min(int(spl[itr]), 10)
        itr += 1
    if 'i' in text:
        if field == 'infobox' or field == 'all':
            counts[3] = min(10, int(spl[itr]))
        itr += 1
    if 'e' in text:
        if field == 'ext' or field == 'all':
            counts[4] = min(10, int(spl[itr]))
        itr += 1
    if 'r' in text:
        if field == 'ref' or field == 'all':
            counts[5] = min(10, int(spl[itr]))
        itr += 1
    #print(counts)
    return counts

def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

def getline(word, field, filename, path_to_index):
    linecount = 0
    #print(word, field)
    line_counts_file = os.path.join(path_to_index, "line_counts.txt")
    f = open(line_counts_file, 'r')
    while True:
        temp_line = f.readline()
        if not temp_line:
            break
        temp_list = temp_line.split(':')
        if temp_list[0] == filename:
            linecount = int(temp_list[1])
            break
    f.close()

    line = ""
   #print(word, " ", linecount, filename)
    full_filename = os.path.join(path_to_index, filename)
    with open(full_filename) as fp:
        for curr_line in fp:
            if curr_line.startswith(word):
                line = curr_line
                break
    #print("parsed")
    if line == "":
        return

    key, index = line.split(':')
    docs = index.split('|')
    word_docs = len(docs)
    idf = math.log10(total_docs/ word_docs)
    #print(idf)
    for doc in docs:
        doc_no, doc_index = doc.split('-')
        doc_no = doc_no[1:]
        counts = get_counts(doc_index, field)
        temp_sum = sum(counts) * idf
        if doc_no not in doc_map:
            doc_map[doc_no] = temp_sum
        else:
            doc_map[doc_no] += temp_sum
        #print(doc_map[doc_no])


def get_list(q, path_to_index, full_query):
    visited = []
    for word, field in q:
        if (word, field) in visited:
            continue
        filename = word[:2] + ".txt"
        final_index_path = os.path.join(path_to_index, filename)
        if not os.path.exists(final_index_path):
            continue
        getline(word, field, filename, path_to_index)
        visited.append((word, field))
    list = sorted(doc_map.items(), reverse=True, key=lambda x: x[1])
    itr = 0
    ans = []
    excludes = ["Wikipedia:", "Help:", "File:", "Template:", "Category:"]
    for i in list:
        if itr == 10:
            break
        if int(i[1]) == 0:
            break
        temp = str(int(i[0]) // 100000)
        id_file_name = "titles-" + temp + ".txt"
        id_file_path = os.path.join(sys.argv[1], id_file_name)
        #print(id_file_path)
        with open(id_file_path) as fp:
            for curr_line in fp:
                if curr_line.startswith(i[0] + ":"):
                    line = curr_line
        #line = linecache.getline(title_path, int(i[0]))
        #print("got line")
        f, colon, title = line.partition(':')
        title = title[:-1]
        if any(ex in title for ex in excludes):
            continue
        #print(i[0], title)
        ans.append(title)
        itr += 1
    return ans
def search_query(query, path_to_index):
    field = ['title:', 'body:', 'category:', 'infobox:', 'ext:', 'ref:']
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
                        q.append((x, field))
    else:
        split = re.split(r"[^A-Za-z0-9]+", query)
        q = []
        for t in split:
            t = stemmer.stemWord(t.lower())
            if t not in stop_words:
                q.append((t, 'all'))
    return get_list(q, path_to_index, query)

def search(path_to_index, query):
    output = search_query(query, path_to_index)
    doc_map.clear()
    return output

def main():
    path_to_index = sys.argv[1]
    while(True):
        more_query = input("Query? y/n:")
        more_query = more_query.lower()
        if more_query == 'n':
            break
        if not more_query == 'y':
            continue
        curr_query = input("Search:")
        start_time = timeit.default_timer()
        output = search(path_to_index, curr_query)
        stop_time = timeit.default_timer()
        print("***********Results************")
        for out in output:
            print(out)
        print("******************************")
        print("Time:", stop_time - start_time, "seconds")


if __name__ == '__main__':
    main()