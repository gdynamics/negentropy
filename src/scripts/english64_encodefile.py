#!/usr/bin/env python
import os, sys

sys.path.append(os.path.abspath('../'))
from english64 import English64

if __name__ == "__main__":
    print('-'*90)
    print('Unencrypted sample file macbeth.txt...')

    print('Reading ../test/macbeth.txt')
    with open('../test/macbeth.txt', 'rb') as f:
        data = f.read()

    print('Converting data to english64')
    data = English64.encode(data)

    print('Writing base64 data to ../test/macbeth.txt.e64')
    with open('../test/macbeth.txt.e64', 'w+') as f:
        f.write(data)

    print('-'*90)
    print('Encrypted sample file macbeth.txt.enc...')

    print('Reading ../test/macbeth.txt.enc')
    with open('../test/macbeth.txt.enc', 'rb') as f:
        data = f.read()

    print('Converting data to english64')
    data = English64.encode(data)

    print('Writing base64 data to ../test/macbeth.txt.enc.e64')
    with open('../test/macbeth.txt.enc.e64', 'w+') as f:
        f.write(data)

    print('-'*90)
