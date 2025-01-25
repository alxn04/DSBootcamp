NUM_OF_STEPS = 3

REPORT_FILENAME = "report"

REPORT_TEMPLATE = """
Отчет
Мы сделали {total} наблюдений при подбрасывании монеты: {tails} из них были решками и {heads} из них были орлами.
Вероятности составляют {tails_percent:.2f}% и {heads_percent:.2f}% соответственно.
Наш прогноз заключается в том, что в следующих {steps} наблюдениях у нас будет: {predicted_tails} решка и {predicted_heads} орел.
"""
LOG_FILENAME = "analytics.log"

API_KEY = "7770683768:AAG64VBzt0t1agzzdh22X9FbSKbNMyN7Wm4"

BOT_URL = "https://api.telegram.org/bot"

CHANNEL_ID = "@s21reports"
