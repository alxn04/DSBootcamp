import sys


def get_name_from_file(filename, email):
    try:
        with open(filename, "r") as file:
            for line in file.readlines():
                split_line = line.split("\t")
                if len(split_line) == 3:
                    if split_line[2][:-1] == email:
                        return split_line[0]
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} is not exists")


def letter_text(name):
    print(
        f"Дорогой {name}, добро пожаловать в нашу команду. Мы уверены, что с вами будет приятно работать. Это обязательное условие для профессионалов, которых нанимает наша компания."
    )


def main():
    try:
        if len(sys.argv) == 2:
            email = sys.argv[1]
            name = get_name_from_file("employees.tsv", email)
            if name:
                letter_text(name)
            else:
                raise Exception("Email not found in file")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
