#!/bin/bash
vacancy_name="$1"
encoded_vacancy_name=$(echo "$vacancy_name" | sed 's/ /%20/g')
curl -s "https://api.hh.ru/vacancies?text=$encoded_vacancy_name&search_field=name&page=1&per_page=20" | jq . > hh.json
