import os
import sys
from random import randint


class Research:
    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):
            heads = 0
            tails = 0
            for result in self.data:
                heads += result[0]
                tails += result[1]
            return [heads, tails]

        def Fractions(self):
            count = self.counts()
            if sum(count) == 0:
                raise ValueError("Division by zero")
            return [count[0] / sum(count) * 100, count[1] / sum(count) * 100]

    class Analytics(Calculations):
        def predict_random(self):
            count_predictions = sum(self.counts())
            predict_list = []
            for _ in range(count_predictions):
                head = randint(0, 1)
                tail = 1 - head
                predict_list.append(list([head, tail]))
            return predict_list

        def predict_last(self):
            return self.data[-1]

    def __init__(self, filename):
        self.filename = filename

    def file_reader(self, has_header=True):
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"File {self.filename} is not exists")
        with open(self.filename, "r") as file:
            lines = file.readlines()
        self.check_csv_file(lines, has_header)

        return [list(map(int, line.strip().split(","))) for line in lines[has_header:]]

    def check_csv_file(self, data, has_header):
        if os.path.splitext(self.filename)[1] != ".csv":
            raise ValueError("File must have .csv extension")
        if len(data) < 2:
            if has_header or len(data) < 1:
                raise ValueError("File must contain as least 2 lines: header and data")
        if has_header:
            header = data[0].strip().split(",")
            if len(header) != 2:
                raise ValueError("Header must contain 2 fields separated by a comma")
        for line in data[has_header:]:
            split_line = line.strip().split(",")
            if len(split_line) != 2 or split_line[0] + split_line[1] not in [
                "10",
                "01",
            ]:
                print()
                raise ValueError(
                    f"Incorrect line in file: '{line[:-1]}'. Line must contain either 1 and 0 or 0 and 1"
                )


def main():
    try:
        if len(sys.argv) == 2:
            researcher = Research(sys.argv[1])
            file = researcher.file_reader()
            print(f"File reader:\n {file}")

            calculator = researcher.Calculations(file)
            counts = calculator.counts()
            fractions = calculator.Fractions()
            print(f"Counts heads and tails:\n {counts[0]}, {counts[1]}")
            print(f"Percentage of heads and tails:\n {fractions[0]}, {fractions[1]}")

            analytics = Research.Analytics(file)
            print(f"Random prediciton list: {analytics.predict_random()}")
            print(f"Last prediction:\n {analytics.predict_last()}")
            print("count:", analytics.counts())

        else:
            raise ValueError("Incorrect input. Check exmaple: first_child.py data.csv")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
