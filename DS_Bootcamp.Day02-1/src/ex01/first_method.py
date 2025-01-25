class Research:
    def __init__(self, filename):
        self.filename = filename
    def file_reader(self):
        try:
            with open(self.filename, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File {self.filename} is not exists")
        except Exception as e:
            print(f"Error: {e}")


def main():
    researcher = Research("data.csv")
    file = researcher.file_reader()
    print(file)

if __name__ == '__main__':
    main()