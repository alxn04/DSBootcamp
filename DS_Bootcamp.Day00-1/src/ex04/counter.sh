#!/bin/bash
path="../ex03/hh_positions.csv"
filename="hh_uniq_positions.csv"
touch tmp_grep.txt
touch tmp.csv
IFS=$'\n'
for line in $(tail -n +2 $path)
do
(echo "$line" | grep -Eo 'Junior|Middle|Senior') >> tmp_grep.txt
done
count_junior=$(grep -c "Junior" tmp_grep.txt)
count_middle=$(grep -c "Middle" tmp_grep.txt)
count_senior=$(grep -c "Senior" tmp_grep.txt)
echo "\"Junior\",$count_junior" >> tmp.csv
echo "\"Middle\",$count_middle" >> tmp.csv
echo "\"Senior\",$count_senior" >> tmp.csv
(sort -rt ',' -k2 tmp.csv) > $filename
sed -i '1s/^/"name","count"\n/' $filename
rm tmp_grep.txt
rm tmp.csv