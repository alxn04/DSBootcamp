num_of_steps = 3

report_filename = "report"

report_template = """
Отчет
Мы сделали {total} наблюдений при подбрасывании монеты: {tails} из них были решками и {heads} из них были орлами.
Вероятности составляют {tails_percent:.2f}% и {heads_percent:.2f}% соответственно.
Наш прогноз заключается в том, что в следующих {steps} наблюдениях у нас будет: {predicted_tails} решка и {predicted_heads} орел.
"""
