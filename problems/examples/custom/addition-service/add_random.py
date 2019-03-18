#!/usr/bin/env python3
import sys

print('What is the sum of {} and {}?'.format(
    str({{value_1}}),
    str({{value_2}})))
print('Input:')
sys.stdout.flush()
res = sys.stdin.readline().strip()
if int(res.strip()) == {{value_1}} + {{value_2}}:
    print('Congratulations! Here is your flag:\n{}'.format(
        '{{flag}}'))
    sys.stdout.flush()
    sys.exit()
else:
    print("Sorry, that's incorrect. Please try again.")
    sys.stdout.flush()
    sys.exit()
