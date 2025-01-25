import os


def print_virtual_env():
    env_path = os.environ.get("VIRTUAL_ENV")  # VIRTUAL_ENV - путь к директории среды
    if env_path:
        print(f"Your current virtual env is {env_path}")
    else:
        print("No virtual environment active.")


if __name__ == "__main__":
    print_virtual_env()
