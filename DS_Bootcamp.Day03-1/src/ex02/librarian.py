import os
import subprocess
import sys

import pkg_resources


def check_virtual_env():
    env_path = os.environ.get("VIRTUAL_ENV")
    if "DS_Bootcamp.Day03-1/src/ex02/lornelvu_2" not in env_path:
        raise EnvironmentError(
            "Необходимо запустить скрипт в правильной виртуальной среде"
        )
    else:
        print(f"Вы находитесь в виртуальном окружении: {env_path}")


def install_libraries():
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def get_libraries():
    return subprocess.check_output(["pip", "freeze"]).decode().strip().split("\n")


def save_requirements(libraries):
    try:
        with open("requirements.txt", "w") as f:
            for item in libraries:
                f.write(item + "\n")
    except IOError as e:
        print(f"Ошибка при записи в файл requirements.txt: {e}")


if __name__ == "__main__":
    try:
        check_virtual_env()
        install_libraries()
        libraries = get_libraries()
        print("Список установленных библиотек:")
        [print(item) for item in libraries]
        save_requirements(libraries)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
