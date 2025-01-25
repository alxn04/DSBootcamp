#!/bin/bash
path="../ex01/hh.csv"
header=$(head -n 1 $path)
tail -n +2 $path | sort -t ',' -k2 -k1n > hh_sort_tmp.csv
echo "$header" > hh_sorted.csv
cat hh_sort_tmp.csv >> hh_sorted.csv
rm hh_sort_tmp.csv
