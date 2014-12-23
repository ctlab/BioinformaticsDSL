#find input files!
find *.txt > inputs.in
#sorting data
sort -n  -o a.sorted a.txt
#get 5 first lines of data
head -5 a.sorted > head.out