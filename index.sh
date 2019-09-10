python indexer.py $1 $2
g++ exsort.cpp -o exsort
./exsort $2
python line_count.py $2
python split_id_title.py $2
