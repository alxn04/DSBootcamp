import logging
import os
from random import randint

import requests
from config import API_KEY, BOT_URL, CHANNEL_ID, LOG_FILENAME


class Research:
    class Calculations:
        def __init__(self, data):
            self.data = data
            logging.info("Initialization of Calculations object")

        def counts(self):
            heads = 0
            tails = 0
            for result in self.data:
                heads += result[0]
                tails += result[1]
            logging.info("Success count of heads and tails")
            return [heads, tails]

        def Fractions(self):
            count = self.counts()
            if sum(count) == 0:
                logging.error("Error while counting of fractions")
                raise ValueError("Division by zero")
            logging.info("Success count fractions of heads and tails")
            return [count[0] / sum(count) * 100, count[1] / sum(count) * 100]

    class Analytics(Calculations):
        def predict_random(self, num_predictions):
            predict_list = []
            for _ in range(num_predictions):
                head = randint(0, 1)
                tail = 1 - head
                predict_list.append(list([head, tail]))
            logging.info("Success predict list of heads and tails")
            return predict_list

        def predict_last(self):
            logging.info("Success predict last result")
            return self.data[-1]

        def save_file(self, filename, extension="txt"):
            try:
                full_filename = f"{filename}.{extension}"
                with open(full_filename, "w") as file:
                    file.write(self.data)
                print(f"Report save into {full_filename}")
                logging.info(f"Success save report to {full_filename}")
                Research.send_to_telegram("The report has been successfully created")
            except Exception as e:
                logging.error(f"Error save report to {full_filename}")
                Research.send_to_telegram(
                    "The report hasn't been created due to an error"
                )
                print(f"Error while save data into {full_filename}")

    def __init__(self, filename):
        self.filename = filename
        self._setup_logging()
        logging.info(f"Initialization Research object with file {filename}")

    def _setup_logging(self):
        logging.basicConfig(
            filename=LOG_FILENAME,
            level=logging.INFO,
            filemode="w",
            format="%(asctime)s %(message)s",
        )
        logging.info(f"BEGIN NEW RUN PROGRAM: Setup logging config")

    def file_reader(self, has_header=True):
        if not os.path.isfile(self.filename):
            logging.error(f"File {self.filename} is not exists")
            raise FileNotFoundError(f"File {self.filename} is not exists")
        with open(self.filename, "r") as file:
            lines = file.readlines()
        self.check_csv_file(lines, has_header)
        logging.info(f"Success read data from {self.filename}")
        return [list(map(int, line.strip().split(","))) for line in lines[has_header:]]

    def check_csv_file(self, data, has_header):
        if os.path.splitext(self.filename)[1] != ".csv":
            logging.error(f"File {self.filename} must have .csv extension")
            raise ValueError("File must have .csv extension")
        if len(data) < 2:
            if has_header or len(data) < 1:
                logging.error(f"Incorrect count of lines in {self.filename}")
                raise ValueError("File must contain as least 2 lines: header and data")
        if has_header:
            header = data[0].strip().split(",")
            if len(header) != 2:
                logging.error(f"Incorrect header in {self.filename}")
                raise ValueError("Header must contain 2 fields separated by a comma")
        for line in data[has_header:]:
            split_line = line.strip().split(",")
            if len(split_line) != 2 or split_line[0] + split_line[1] not in [
                "10",
                "01",
            ]:
                logging.error(f"Incorrect line in {self.filename}: '{line[:-1]}'")
                raise ValueError(
                    f"Incorrect line in file: '{line[:-1]}'. Line must contain either 1 and 0 or 0 and 1"
                )
        logging.info(f"Success check csv structure of {self.filename}")

    def send_to_telegram(message):
        token = API_KEY
        url = BOT_URL
        channel_id = CHANNEL_ID
        url += token
        method = url + "/sendMessage"
        r = requests.post(method, data={"chat_id": channel_id, "text": message})
        if r.status_code != 200:
            logging.error("Error while sending message to telegram channel")
            raise Exception("Error while sending message to telegram channel")
        logging.info("Success send message to telegram channel")
