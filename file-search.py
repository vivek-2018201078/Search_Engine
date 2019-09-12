import sys
from Stemmer import Stemmer
import re
from operator import add
import os
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
            counts[0] = 400
        itr += 1
    if 'b' in text:
        if field == 'body' or field == 'all':
            counts[1] = min(200, int(spl[itr]))
        itr += 1
    if 'c' in text:
        if field == 'category' or field == 'all':
            counts[2] = min(10, int(spl[itr]))
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
    return counts

def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

def getline(word, field, filename):
    linecount = 0
    line_counts_file = os.path.join(sys.argv[1], "line_counts.txt")
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

    # low = 1
    # high = linecount
    line = ""
   #print(word, " ", linecount, filename)
    full_filename = os.path.join(sys.argv[1], filename)
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
    idf = math.log10(total_docs / word_docs)
    for doc in docs:
        doc_no, doc_index = doc.split('-')
        doc_no = doc_no[1:]
        counts = get_counts(doc_index, field)
        temp_sum = sum(counts) * idf
        if doc_no not in doc_map:
            doc_map[doc_no] = temp_sum
        else:
            doc_map[doc_no] += temp_sum


def get_list(q, path_to_index, title_path):
    for word, field in q:
        filename = word[:2] + ".txt"
        final_index_path = os.path.join(path_to_index, filename)
        if not os.path.exists(final_index_path):
            continue
        getline(word, field, filename)


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
        ans.append(title)
        itr += 1
    return ans
def search_query(query, path_to_index, title_path):
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
    return get_list(q, path_to_index, title_path)

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
    #final_index_path = os.path.join(path_to_index, 'final.txt')
    title_path = os.path.join(path_to_index, 'id_title_map.txt')
    output = []
    for query in queries:
        temp = search_query(query, path_to_index, title_path)
        output.append(temp)
        #print("QUERY DONE...")
        doc_map.clear()
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