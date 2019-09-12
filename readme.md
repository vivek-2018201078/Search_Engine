# Wikipedia Search Engine
Search Engine on large wikipedia dump with support for field queries

## Requirements:
Run in project environment provided at "environment.yml". Install using conda.

## Indexing
To make index of xml file, run
```bash
./index.sh path_to_wiki_dump path_to_index_folder
```
sample wikipedia dump provided in data folder

## Searching
Searching queries one by one:
```python
python search.py path_to_index_folder
```
In Python interface type "y" for more query then actual query. 'n' to abort.

For file as query input and to store results in file-
```bash
./search.sh path_to_index_folder path_to_query_file path_to_output_file
```
Query input is given line by line in file.
Top 10 results are retrieved and stored in file.

### Field Query tokens
To search 'x' in particular field:

Title - "title:x"  
Body - "body:x"  
Category - "category:x"  
Infobox - "infobox:x"  
External Links - "ext:x"  
References - "ref:x"
