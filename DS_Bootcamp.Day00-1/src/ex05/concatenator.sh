#!/bin/bash
filename="data.csv"
header=$(head -n 1 "../ex03/hh_positions.csv")
echo "$header" > $filename
for file in ../ex05/2024*.csv; do
    if [ -f "$file" ]; then
        for line in $(tail -n +2 $file); do
            echo $line >> $filename
       
        done 
        
    fi
done