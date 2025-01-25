Создать виртуальное окружение в каталоге:
python3 -m venv lornelvu

Активировать виртуальное окружение:
source lornelvu/bin/activate

Деактивировать:
deactivate

Для профилирования программ:
-s сортировка по убыванию
python -m cProfile -s time financial_enhanced.py MSFT 'Total Revenue' > profiling-http.txt

Отсортировать по убыванию количества вызовов:
python -m cProfile -s calls financial_enhanced.py MSFT 'Total Revenue' > profiling-http.txt

Создать файл который будем читать с помощью pstats
python -m cProfile -o profiling_stats.prof financial_enhanced.py
python -m pstats profiling_stats.prof | tee pstats-cumulative.txt

далее в интерактивной консоли ввести:
sort cumtime
stats 5