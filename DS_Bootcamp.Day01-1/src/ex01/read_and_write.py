def read_csv():
    try:
        with open('ds.csv', 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        raise FileNotFoundError("File ds.csv is not exists")
    except Exception as e:
        print(f"Error in read_csv(): {e}")


def write_tsv(lines):
    try:
        with open('ds.tsv', 'w') as file:
            for line in lines:
                file.write(line)
    except Exception as e:
        print(f"Error in write_csv(): {e}")

def process_line(line):
    try:
        new_line = []
        inside_quotes = False
        i = 0
        for i in range(len(line)):
            char = line[i]
            if char == '"':
                inside_quotes = not inside_quotes
                new_line.append(char)
            elif char == ',' and not inside_quotes:
                new_line.append('\t')
            else:
                new_line.append(char)
        return ''.join(new_line)
    except Exception as e:
        print(f"Error in process_line(): {e}")

def main():
    try:
        lines = read_csv() 
        processed_lines = [process_line(line) for line in lines]
        write_tsv(processed_lines) 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()