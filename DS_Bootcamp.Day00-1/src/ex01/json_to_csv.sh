#!/bin/bash
vacancy_name="$1"
encoded_vacancy_name=$(echo "$vacancy_name" | sed 's/ /%20/g')
api_url="https://api.hh.ru/vacancies?text=$encoded_vacancy_name&search_field=name&page=1&per_page=20"
curl -s "$api_url" | jq -f filter.jq | jq -r '[.id, .created_at, (.name | gsub(","; " ")), .has_test, .alternate_url] | @csv' > hh.csv
sed -i '1s/^/"id","created_at","name","has_test","alternate_url"\n/' hh.csv