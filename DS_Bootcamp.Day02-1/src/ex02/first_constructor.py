import sys
import os

class Research:
    def __init__(self, filename):
        self.filename = filename

    def file_reader(self):
            if not os.path.isfile(self.filename):
                raise FileNotFoundError(f"File {self.filename} is not exists")
            with open(self.filename, 'r') as file:
                lines = file.readlines()
            self.check_csv_file(lines)

            return lines

    def check_csv_file(self, data):
        if os.path.splitext(self.filename)[1] != '.csv':
            raise ValueError("File must have .csv extension")
        if len(data) < 2:
            raise ValueError("File must contain as least 2 lines: header and data")
        header = data[0].strip().split(',')
        if len(header) != 2:
            raise ValueError("Header must contain 2 fields separated by a comma")
        for line in data[1:]:
            split_line = line.strip().split(',')
            if len(split_line) != 2 or split_line[0] + split_line[1] not in ['10','01']:
                print()
                raise ValueError(f"Incorrect line in file: '{line[:-1]}'. Line must contain either 1 and 0 or 0 and 1")


def main():
    try:
        if (len(sys.argv) == 2):
            researcher = Research(sys.argv[1])
            file = researcher.file_reader()
            for line in file:
                print(line.strip())
        else:
            raise ValueError("Incorrect input. Check exmaple: first_constructor.py data.csv")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()