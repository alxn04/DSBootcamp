import sys


def read_file(filename):
    try:
        with open(filename, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} is not exists")


# Проверка формата
# 1. имя и фамилия разделены точкой
# 2. присутствует @
# 3. домен отделен точкой
def check_format(line):
    is_correct = 1
    check_list = line.split(".")
    if len(check_list) != 3 or "@" not in check_list[1]:
        is_correct = 0
    return is_correct


def create_tsv_table(data):
    with open("employees.tsv", mode="w") as file:
        header = "Name\tSurname\tE-mail\n"
        file.write(header)
        for line in data:
            if check_format(line):
                first_name = line.split(".")[0].title()
                last_name = line.split(".")[1].title().split("@")[0]
                file.write(f"{first_name}\t{last_name}\t{line}\n")
            else:
                raise Exception(f"Incorrect line in file: {line}")


def main():
    try:
        if len(sys.argv) == 2:
            data = read_file(sys.argv[1])
            create_tsv_table(data)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
