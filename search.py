import sys
from Stemmer import Stemmer
from nltk.corpus import stopwords

stemmer = Stemmer('english')
stop_words = list(stopwords.words('english'))

doc_map = {}

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
    final_index_path = path_to_index + '/final.txt'
    title_path = path_to_index + '/id_title_map.txt'


def main():
    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)


if __name__ == '__main__':
    main()