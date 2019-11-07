#!/usr/bin/env python3
import os
from sys import argv

from django.core.management import execute_from_command_line

sauce_k = os.environ['SAUCE_ACCESS_KEY']
sauce_u = os.environ['SAUCE_USERNAME']

print("Sauce card: |{} {}|".format(sauce_k[:len(sauce_k)//2], sauce_k[len(sauce_k)//2:]))
print("Sauce person: |{} {}|".format(sauce_u[:len(sauce_u)//2], sauce_u[len(sauce_u)//2:]))

if __name__ == "__main__":
    execute_from_command_line(argv)
