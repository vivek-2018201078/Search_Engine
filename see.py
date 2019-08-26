import xml.etree.ElementTree as etree
import sys
import re
from nltk.corpus import stopwords
from Stemmer import Stemmer
from nltk.stem import PorterStemmer
import queue as Q

stemmer = Stemmer('english')
ps = PorterStemmer()
stop_words = list(stopwords.words('english'))

xml_loc = sys.argv[1]
index_folder = sys.argv[2]

page_map = {}
key_map = {}
id_title_map = {}
page_count = 0
file_count = 0
store_step = 1000


def write_to_index():
    file = open(index_folder + '/file' + str(file_count), "w")
    file2 = open(index_folder + '/id_title_map', "a+")
    for key in sorted(key_map.keys()):
        file.write(str(key) + ':' + str(key_map[key]) + '\n')
    for key in id_title_map.keys():
        file2.write(str(key) + ':' + str(id_title_map[key]) + '\n')

##get proper tag without {}
def get_tag(el):
    loc = el.rfind('}')
    if loc >= 0:
        el = el[loc + 1:]
    return el

#returns stemmed keys from string as list
def get_keys(string):
    l = []
    split = re.split(r"[^A-Za-z0-9]+", string)
    for t in split:
        t = stemmer.stemWord(t.lower())
        if t not in stop_words:
            l.append(t)
    return l

def get_keys_linewise(text):
    data = text.split("\n")
    l = []
    for line in data:
        if '{{' in line or '}}' in line or 'http' in line or '[[Categorry:' in line:
            continue
        temp = []
        split = re.split(r"[^A-Za-z0-9]+", line)
        for t in split:
            t = stemmer.stemWord(t.lower())
            if t not in stop_words:
                temp.append(t)
        l = l + temp
    return l

def get_cats(string):
    category_detection = re.compile(u"\[\[Category:(.*?)\]\]", re.M)
    cate = []
    matches = re.finditer(category_detection, string)
    if matches:
        for match in matches:
            temp = match.group(1).split("|")
            if temp:
                cat_keys = get_keys(str(temp))
                for key in cat_keys:
                    if key == '':
                        continue
                    if key not in page_map:
                        page_map[key] = [0, 0, 1, 0]
                    else:
                        page_map[key][2] += 1


def update_key_map():
    for key in page_map:
        if key == '':
            continue
        title = page_map[key][0]
        body = page_map[key][1]
        category = page_map[key][2]
        #id_mapping()
        out = 'd' + str(page_count) + '-'

        if title > 0:
            out = out + 't' + str(title)
        if body > 0:
            out = out + 'b' + str(body)
        if category > 0:
            out = out + 'c' + str(category)

        if key not in key_map:
            key_map[key] = out
        else:
            key_map[key] = key_map[key] + '|' + out





title = None
id = None
revision = False


## title = 0
## body = 1
##
for event, elem in etree.iterparse(xml_loc, events = ('start', 'end')):
    tag = get_tag(elem.tag)

    if event == 'start':
        if tag == 'page':
            page_count += 1
            page_map.clear()
            title = None
            id = None
            revision = False
        elif tag == 'revision':
            revision = True

    else:
        if tag == 'title':
            title = str(elem.text)
            id_title_map[page_count] = title
            title_keys = get_keys(title)
            for key in title_keys:
                if key not in page_map:
                    page_map[key] = [1, 0, 0, 0]
                else:
                    page_map[key][0] += 1
        elif tag == 'id' and revision == False:
            id = int(elem.text)

        elif tag == 'text':
            if elem.text is None:
                continue

            body_keys = get_keys_linewise(str(elem.text))
            for key in body_keys:
                if not key.isnumeric():
                    if len(key) <= 25:
                        if key not in page_map:
                            page_map[key] = [0, 1, 0, 0]
                        else:
                            page_map[key][1] += 1

            #updates page map as well
            get_cats(str(elem.text))

            update_key_map()

        elif tag == 'page':
            if page_count % store_step == 0:
                write_to_index()
                elem.clear()
                page_map.clear()
                key_map.clear()
                id_title_map.clear()
                file_count += 1
                print("file ", file_count)

        elem.clear()

file3 = open(index_folder + '/no_of_files', 'w')
file3.write(str(file_count))
file3.close()