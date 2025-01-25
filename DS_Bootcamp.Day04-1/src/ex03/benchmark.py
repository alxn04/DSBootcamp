import timeit
import sys
from functools import reduce

def get_sum_base(ch):
    sum = 0
    for i in range(0, ch + 1):
        sum += pow(i, 2)
    return sum
def get_sum_reduce(ch):
    return reduce(lambda x, y: x + pow(y, 2), list(range(0, ch+1)))

if __name__ == '__main__':
    functions = {
        'loop' : get_sum_base,
        'reduce' : get_sum_reduce,
    }
    try:
        if (len(sys.argv) == 4):
            function_name = sys.argv[1]
            times = int(sys.argv[2])
            value = int(sys.argv[3])
            func = functions.get(function_name)
            if func is None:
                raise Exception("Incorrect function. Available functions: loop, reduce")
            func_time = timeit.timeit(
                lambda: func(value),
                number = times
            )
            print(func_time)
            print(func(5))

        else:
            raise Exception("Incorrect arguments. Try [script_name] [function] [times]")
    except Exception as e:
        print(f"Error: {e}")
    
