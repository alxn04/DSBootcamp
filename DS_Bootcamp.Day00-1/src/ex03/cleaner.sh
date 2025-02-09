#!/bin/bash
path="../ex02/hh_sorted.csv"
header=$(head -n 1 $path)
echo "$header" > hh_positions.csv
IFS=$'\n'
for line in $(tail -n +2 $path)
do
id=$(echo "$line" | awk -F ',' '{print $1}')
date=$(echo "$line" | awk -F ',' '{print $2}')
name=$(echo "$line" | awk -F ',' '{print $3}')
active=$(echo "$line" | awk -F ',' '{print $4}')
link=$(echo "$line" | awk -F ',' '{print $5}')
match=$(echo "$name" | grep -Eo 'Junior|Middle|Senior' | tr '\n' '/' | sed 's/\/$//')
if [ -z "$match" ]; then
    match='-'
fi
new_line="$id,$date,\"$match\",\"$active\",$link"
echo $new_line >> hh_positions.csv
done



