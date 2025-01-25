class Must_read:
    def __init__(self, filename):
        self.filename = filename
    def read_file(self):
        try:
            with open(self.filename, "r") as file:
                print(file.read())
        except FileNotFoundError:
            print(f"Error: File {self.filename} is not exists")
        except Exception as e:
            print(f"Error: {e}")


def main():
    reader = Must_read("data.csv")
    reader.read_file()

if __name__ == '__main__':
    main()