import sys


def encode(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr(start + (ord(char) - start + shift) % 26)
        else:
            result += char
    return result


def decode(text, shift):
    return encode(text, -shift)


def check_text(text):
    for char in text:
        if ord(char) >= 128:
            raise Exception("Russian language is not supported now")


def main():
    try:
        if len(sys.argv) == 4:
            method = sys.argv[1]
            text = sys.argv[2]
            shift = int(sys.argv[3])
            check_text(text)
            if method == "encode":
                result = encode(text, shift)
                print(result)
            elif method == "decode":
                result = decode(text, shift)
                print(result)
            else:
                raise Exception("Incorrect method (first argument)")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
