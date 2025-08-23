#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


# ensure the project 'src' directory (this file's directory) is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # .../Personal-finance-tracker/src
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_tracker.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
