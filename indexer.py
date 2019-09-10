import xml.etree.ElementTree as etree
import sys
import re
from nltk.corpus import stopwords
from Stemmer import Stemmer
from nltk.stem import PorterStemmer
import os


stemmer = Stemmer('english')
#ps = PorterStemmer()
#stop_words = list(stopwords.words('english'))

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
xml_loc = sys.argv[1]
index_folder = sys.argv[2]

title_total = 0
body_total = 0
category_total = 0
infobox_total = 0
external_total = 0
reference_total = 0

page_map = {}
key_map = {}
id_title_map = {}
page_count = 0
file_count = 0
store_step = 10000


def write_to_index():
    filename = 'file' + str(file_count) + '.txt'
    mapping_file = 'id_title_map.txt'
    file = open(os.path.join(index_folder, filename), "w")
    file2 = open(os.path.join(index_folder, mapping_file), "a+")
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


def get_infobox(text):
    global infobox_total
    data = re.findall(r'{{Infobox(.*?)}}', text, re.DOTALL)
    if not data:
        return
    l = []
    for dat in data:
        temp = get_keys(dat)
        l = l + temp
    infobox_total += len(l)
    if len(l) > 0:
        for key in l:
            if key != '':
                if key not in page_map:
                    page_map[key] = [0, 0, 0, 1, 0, 0]
                else:
                    page_map[key][3] += 1


def get_references(text):
    global reference_total
    data = re.findall(r'==References==(.*?)}}\n\n', text, re.DOTALL)
    if not data:
        return
    data = data[0]
    reference_keys = get_keys(data)
    reference_total += len(reference_keys)
    for key in reference_keys:
        if key not in page_map:
            page_map[key] = [0, 0, 0, 0, 0, 1]
        else:
            page_map[key][5] += 1


def get_keys_linewise(text):
    data = text.split("\n")
    l = []
    for line in data:
        temp = []
        split = re.split(r"[^A-Za-z0-9]+", line)
        for t in split:
            t = stemmer.stemWord(t.lower())
            if t not in stop_words:
                temp.append(t)
        l = l + temp
    return l

def get_cats(text):
    global category_total
    data = re.findall(r'\[\[Category:(.*?)\]\]',  text, re.DOTALL)
    if not data:
        return
    for dat in data:
        cat_keys = get_keys(dat)
        category_total += len(cat_keys)
        for key in cat_keys:
            if key == '':
                continue
            if key not in page_map:
                page_map[key] = [0, 0, 1, 0, 0, 0]
            else:
                page_map[key][2] += 1


def update_key_map():
    for key in page_map:
        if len(key) <= 1:
            continue
            
        title = page_map[key][0]
        body = page_map[key][1]
        category = page_map[key][2]
        infobox = page_map[key][3]
        external_links = page_map[key][4]
        references = page_map[key][5]
        #id_mapping()
        out = 'd' + str(page_count) + '-'

        if title > 0:
            out = out + 't' + str(title)
        if body > 0:
            out = out + 'b' + str(body)
        if category > 0:
            out = out + 'c' + str(category)
        if infobox > 0:
            out = out + 'i' + str(infobox)
        if external_links > 0:
            out = out + 'e' + str(external_links)
        if references > 0:
            out = out + 'r' + str(references)

        if key not in key_map:
            key_map[key] = out
        else:
            key_map[key] = key_map[key] + '|' + out





title = None
id = None


## title = 0
## body = 1
##category = 2
## infobox = 3
## external links = 4
## references = 5
print("Creating intermediate posting lists...")
for event, elem in etree.iterparse(xml_loc, events = ('start', 'end')):
    tag = get_tag(elem.tag)

    if event == 'start':
        if tag == 'page':
            page_count += 1
            page_map.clear()
            title = None
            id = None

    else:
        if tag == 'title':
            title = str(elem.text)
            id_title_map[page_count] = title
            title_keys = get_keys(title)
            title_total += len(title_keys)
            for key in title_keys:
                if key not in page_map:
                    page_map[key] = [1, 0, 0, 0, 0, 0]
                else:
                    page_map[key][0] += 1

        elif tag == 'text':
            if elem.text is None:
                continue

            data = str(elem.text)
            #updates page map as well
            get_infobox(data)
            data = re.compile(r'{{Infobox(.*?)}}\n\n', re.DOTALL).sub(' ', data)
            get_cats(data)
            get_references(data)

            external_index = 0
            category_index = len(data)
            reference_index = 0
            try:
                external_index = data.index('==External links==') + 20
            except:
                pass
            try:
                category_index = data.index('[[Category:')
            except:
                pass
            try:
                reference_index = data.index('==References==')
            except:
                pass
            if external_index:
                external_data = data[external_index:category_index]
                external_keys = get_keys(external_data)
                external_total += len(external_keys)
                for key in external_keys:
                    if key not in page_map:
                        page_map[key] = [0, 0, 0, 0, 1, 0]
                    else:
                        page_map[key][4] += 1
            if reference_index:
                data = data[:reference_index]
            elif external_index:
                data = data[:external_index - 20]
            elif category_index:
                data = data[:category_index]
            body_keys = get_keys(data)
            body_total += len(body_keys)
            for key in body_keys:
                if len(key) <= 25:
                    if key not in page_map:
                        page_map[key] = [0, 1, 0, 0, 0, 0]
                    else:
                        page_map[key][1] += 1
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

write_to_index()
page_map.clear()
key_map.clear()
id_title_map.clear()
file_count += 1
print("Total intermediate files:", file_count)
file_count_file = 'no_of_files.txt'
file3 = open(os.path.join(index_folder, file_count_file), 'w')
file3.write(str(file_count))
file3.close()

# print("title = ", title_total / page_count)
# print("body = ", body_total / page_count)
# print("category = ", category_total / page_count)
# print("infobox = ", infobox_total / page_count)
# print("external_links = ", external_total / page_count)
# print("references = ", reference_total)