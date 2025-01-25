#!/bin/bash
path="../ex03/hh_positions.csv"
header=$(head -n 1 "$path")
IFS=$'\n'
for line in $(tail -n +2 "$path"); do
    id=$(echo "$line" | awk -F ',' '{print $1}')
    created_at=$(echo "$line" | awk -F ',' '{print $2}')
    name=$(echo "$line" | awk -F ',' '{print $3}')
    has_test=$(echo "$line" | awk -F ',' '{print $4}')
    alternate_url=$(echo "$line" | awk -F ',' '{print $5}')

    date=$(echo "$created_at" | awk -F 'T' '{print $1}')
    date=${date#\"} # убрать кавычку в начале

    output_file="$date.csv"
    if [ ! -f "$output_file" ]; then
        echo "$header" > "$output_file"
    fi
    echo "$id,$created_at,$name,$has_test,$alternate_url" >> "$output_file"
done