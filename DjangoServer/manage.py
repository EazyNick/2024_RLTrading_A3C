#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
from pathlib import Path

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoServer.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # # 추가된 부분: main.py 실행
    # def run_my_function():
    #     import main  # main.py를 임포트하고 실행
    #     main.Run()

    # # 스레드를 사용하여 main.py의 함수를 실행
    # thread = threading.Thread(target=run_my_function)
    # thread.daemon = True
    # thread.start()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()