#!/usr/bin/python3

import sys

def binwalk_entropy(file):
    pass

if __name__ == "__main__":
    print(len(sys.argv))

    if len(sys.argv) != 3:
        raise ValueError("Two files, please")
    
    binwalk_entropy(sys.argv[1])

