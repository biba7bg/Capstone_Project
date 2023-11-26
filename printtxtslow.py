import sys
import time

def print_slow(s):
    for c in s + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.7/10)
        
def separate():
    for letter in "*************************":
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.3/10)
    print()