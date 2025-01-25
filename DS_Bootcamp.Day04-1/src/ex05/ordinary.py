import sys
import resource

def get_list_from_file(file_name):
    try:
        with open (file_name, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return []
    except IOError as e:
        print(f"Error: There was an issue reading the file '{file_name}'. {e}")
        return []

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            file_name = sys.argv[1]
            lines = get_list_from_file(file_name)
            for line in lines:
                pass
            peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**3
            user_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
            system_time = resource.getrusage(resource.RUSAGE_SELF).ru_stime
            total_time = user_time + system_time

            print(f"Peak Memory Usage = {peak_memory:.3f} GB")
            print(f"User Mode Time + System Mode Time = {total_time:.2f}s")
        else:
            raise Exception("Incorrect arguments. Try [script_name] [file_name]")
    except Exception as e:
        print(f"Error: {e}")
