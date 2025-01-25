import timeit

def get_gmail_base(list):
    emails = []
    for email in list:
        if email.endswith('gmail.com'):
            emails.append(email)
    return emails

def get_gmail_comprehension(list):
    return [email for email in list if email.endswith('gmail.com')]

def get_gmail_map(emails):
    return list(map(lambda email: email if email.endswith('gmail.com') else emails.remove(email), 
                    emails))

if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
                'anna@live.com', 'philipp@gmail.com'] * 5
    try:
        base_time = timeit.timeit(
            lambda: get_gmail_base(emails),
            number = 1000000
        )
        comprehension_time = timeit.timeit(
            lambda: get_gmail_comprehension(emails),
            number = 1000000
        )
        map_time = timeit.timeit(
            lambda: get_gmail_map(emails),
            number = 1000000
        )

        if map_time <= base_time and map_time <= comprehension_time:
            print("it is better to use a map")
        elif comprehension_time <= base_time and comprehension_time <= map_time:
            print("it is better to use a list comprehension")
        else: 
            print("it is better to use a list iteration")

        times = sorted([base_time, comprehension_time, map_time])
        print(f"{times[0]} vs {times[1]} vs {times[2]}")
    except Exception as e:
        print(f"Error: {e}")
    
