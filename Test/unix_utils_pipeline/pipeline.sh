#find input files
find *.txt > sort.out
#sorting data
sort -n  -o sorted.out a.txt
#get 5 first lines of data
head -5 sorted.out > head.out