import timeit
import random
from collections import Counter

def get_dict_base(values):
    counts = {key: 0 for key in range(101)}
    for i in values:
        counts[i] += 1
    return counts

def get_dict_counter(values):
    return Counter(values)

def get_top_dict_base(values, n = 10):
    count_dict = get_dict_base(values)
    top_numbers = sorted(count_dict.items(), key = lambda x: x[1], reverse = True)
    return [i[0] for i in top_numbers[:n]]

def get_top_dict_counter(values, n = 10):
    return Counter(values).most_common(n)

if __name__ == '__main__':
    try:
        random_list = [random.randint(0,100) for _ in range(1000000)]
       
        base_dict_time = timeit.timeit(
            lambda: get_dict_base(random_list),
            number = 1
        )
        counter_dict_time = timeit.timeit(
            lambda: get_dict_counter(random_list),
            number = 1
        )
        base_top_time = timeit.timeit(
            lambda: get_top_dict_base(random_list),
            number = 1
        )
        counter_top_time = timeit.timeit(
            lambda: get_top_dict_counter(random_list),
            number = 1
        )

        print(f"""my function: {base_dict_time}
Counter: {counter_dict_time}
my top: {base_top_time}
Counter`s top: {counter_top_time}""")
         
    except Exception as e:
        print(f"Error: {e}")
    
