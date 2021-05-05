#!/usr/bin/env python
import os, sys

sys.path.append(os.path.abspath('../'))
from b64 import B64

if __name__ == "__main__":
    print('-'*90)
    print('Unencrypted sample file macbeth.txt...')

    print('Reading ../test/macbeth.txt')
    with open('../test/macbeth.txt', 'rb') as f:
        data = f.read()

    print('Converting data to base64 with padding')
    data = B64.encode(data)

    print('Writing base64 data to ../test/macbeth.txt.b64')
    with open('../test/macbeth.txt.b64', 'w+') as f:
        f.write(data)

    print('-'*90)
    print('Encrypted sample file macbeth.txt.enc...')
    
    print('Reading ../test/macbeth.txt.enc')
    with open('../test/macbeth.txt.enc', 'rb') as f:
        data = f.read()

    print('Converting data to base64 with padding')
    data = B64.encode(data)

    print('Writing base64 data to ../test/macbeth.txt.enc.b64')
    with open('../test/macbeth.txt.enc.b64', 'w+') as f:
        f.write(data)

    print('-'*90)
