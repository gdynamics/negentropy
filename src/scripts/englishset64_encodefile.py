#!/usr/bin/env python
import os, sys

sys.path.append(os.path.abspath('../'))
from englishset64 import EnglishSet64

if __name__ == "__main__":
    print('-'*90)
    print('Unencrypted sample file macbeth.txt...')

    print('Reading ../test/macbeth.txt')
    with open('../test/macbeth.txt', 'rb') as f:
        data = f.read()

    print('Converting data to englishset64')
    data = EnglishSet64.encode(data)

    print('Writing base64 data to ../test/macbeth.txt.es64')
    with open('../test/macbeth.txt.es64', 'w+') as f:
        f.write(data)

    print('-'*90)
    print('Encrypted sample file macbeth.txt... (1)')

    print('Reading ../test/macbeth.txt.enc')
    with open('../test/macbeth.txt.enc', 'rb') as f:
        data = f.read()

    print('Converting data to englishset64')
    data = EnglishSet64.encode(data)

    print('Writing base64 data to ../test/macbeth.txt.enc.es64.1')
    with open('../test/macbeth.txt.enc.es64.1', 'w+') as f:
        f.write(data)

    print('-'*90)
    print('Encrypted sample file macbeth.txt... (2)')

    print('Reading ../test/macbeth.txt.enc')
    with open('../test/macbeth.txt.enc', 'rb') as f:
        data = f.read()

    print('Converting data to englishset64')
    data = EnglishSet64.encode(data)

    print('Writing base64 data to ../test/macbeth.txt.enc.es64.2')
    with open('../test/macbeth.txt.enc.es64.2', 'w+') as f:
        f.write(data)

    print('-'*90)
