def to_dictionary():
    list_of_tuples = [
        ("Russia", "25"),
        ("France", "132"),
        ("Germany", "132"),
        ("Spain", "178"),
        ("Italy", "162"),
        ("Portugal", "17"),
        ("Finland", "3"),
        ("Hungary", "2"),
        ("The Netherlands", "28"),
        ("The USA", "610"),
        ("The United Kingdom", "95"),
        ("China", "83"),
        ("Iran", "76"),
        ("Turkey", "65"),
        ("Belgium", "34"),
        ("Canada", "28"),
        ("Switzerland", "26"),
        ("Brazil", "25"),
        ("Austria", "14"),
        ("Israel", "12"),
    ]
    res_dict = dict(list_of_tuples)
    sorted_dict = sorted(res_dict.items(), key=lambda item: (-int(item[1]), item[0]))
    for item in sorted_dict:
        print(item[0])


def main():
    try:
        to_dictionary()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
