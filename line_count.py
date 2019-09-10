import linecache
import sys
import os
import glob
index_path = sys.argv[1]
line_counts_file = os.path.join(index_path, "line_counts.txt")
files = os.listdir(index_path)
print(files)

def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

for file in files:
    full_path = os.path.join(index_path, file)
    with open(full_path, "r",encoding="utf-8",errors='ignore') as f:
        linecount = sum(bl.count("\n") for bl in blocks(f))
    temp = file + ":" + str(linecount) + "\n"
    print(temp)
    f = open(line_counts_file, "a+")
    f.write(temp)

f.close()
