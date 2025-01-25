import timeit

def get_gmail_base(list):
    emails = []
    for email in list:
        if email.endswith('gmail.com'):
            emails.append(email)
    return emails

def get_gmail_comprehension(list):
    return [email for email in list if email.endswith('gmail.com')]

if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
                'anna@live.com', 'philipp@gmail.com'] * 5
    try:
        base_time = timeit.timeit(
            lambda: get_gmail_base(emails),
            number = 10000000
        )
        comprehension_time = timeit.timeit(
            lambda: get_gmail_comprehension(emails),
            number = 10000000
        )
        if comprehension_time <= base_time:
            print("it is better to use a list comprehension")
        else:
            print("it is better to use a list iteration")
        times = sorted([base_time, comprehension_time])
        print(f"{times[0]} vs {times[1]}")
    except Exception as e:
        print(f"Error: {e}")
    
