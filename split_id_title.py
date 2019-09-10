import sys
import os

folder_path = sys.argv[1]
itr = 1
full_path = os.path.join(folder_path, "id_title_map.txt")

with open(full_path) as fp:
    for line in fp:
        filename = "titles-" + str(itr // 100000) + ".txt"
        full_filename = os.path.join(folder_path, filename)
        file = open(full_filename, 'a+')
        id = int(line.split(':')[0])
        file.write(line)
        itr += 1
