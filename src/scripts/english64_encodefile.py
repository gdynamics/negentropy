#!/usr/bin/env python
import os, sys

sys.path.append(os.path.abspath('../'))
from b64 import B64

if __name__ == "__main__":
    print('-'*90)

    print('Reading ../test/macbeth.txt')
    with open('../test/macbeth.txt', 'r') as f:
        data = f.read()

    print('Converting data to base64 with padding')
    data = B64.encode(data)

    print('Writing base64 data to ../test/macbeth.txt.b64')
    with open('../test/machbeth.txt.b64', 'w+') as f:
        f.write(data)

    print('-'*90)
