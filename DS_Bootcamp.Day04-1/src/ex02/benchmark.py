import timeit
import sys

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

def get_gmail_filter(emails):
    return list(filter(lambda email: email.endswith('gmail.com'), emails))

if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
                'anna@live.com', 'philipp@gmail.com'] * 5
    functions = {
        'loop' : get_gmail_base,
        'list comprehension' : get_gmail_comprehension,
        'map' : get_gmail_map,
        'filter' : get_gmail_filter
    }
    try:
        if (len(sys.argv) == 3):
            function_name = sys.argv[1]
            times = int(sys.argv[2])
            func = functions.get(function_name)
            if func is None:
                raise Exception("Incorrect function. Available functions: loop, list comprehension, map, filter")
            func_time = timeit.timeit(
                lambda: func(emails),
                number = times
            )
            print(func_time)

        else:
            raise Exception("Incorrect arguments. Try [script_name] [function] [times]")
    except Exception as e:
        print(f"Error: {e}")
    
