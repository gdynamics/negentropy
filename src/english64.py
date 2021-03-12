#!/usr/bin/env python
from mappedtranscoder import MappedTranscoder
import base64 # Just for testing

class english64(MappedTranscoder):
    mapping = {
             0: 'the',   1: 'of',    2: 'to',    3: 'and',
             4: 'a',     5: 'in',    6: 'is',    7: 'it',
             8: 'you',   9: 'that', 10: 'he',   11: 'was',
            12: 'for',  13: 'on',   14: 'are',  15: 'with',
            16: 'as',   17: 'I',    18: 'his',  19: 'they',
            20: 'be',   21: 'at',   22: 'one',  23: 'have',
            24: 'this', 25: 'from', 26: 'or',   27: 'had',
            28: 'by',   29: 'not',  30: 'word', 31: 'but',
            32: 'what', 33: 'some', 34: 'we',   35: 'can',
            36: 'out',  37: 'other',38: 'were', 39: 'all',
            40: 'there',41: 'when', 42: 'up',   43: 'use',
            44: 'your', 45: 'how',  46: 'said', 47: 'an',
            48: 'each', 49: 'she',  50: 'which',51: 'do',
            52: 'their',53: 'time', 54: 'if',   55: 'will',
            56: 'way',  57: 'about',58: 'many', 59: 'then',
            60: 'them', 61: 'write',62: 'would',63: 'like',
    }

    def encode(plaintxt: str) -> str:
        ciphertxt = ""
        plainint = [ord(x) for x in plaintxt]
        leng = len(plainint)

        for i in range(0, len(plainint), 3):
            padded = False
            
            # First
            first = (plainint[i] & 0xFD) >> 2
            first = B64.mapping[first]

            # Second
            carry = (plainint[i] & 0x03) << 4
            if i+1 > leng-1:
                padded = True
                second = carry
            else:
                second = carry | ((plainint[i+1] & 0xF0) >> 4)
            second = B64.mapping[second]

            # Third
            if padded:
                third = "="
            else:
                carry = (plainint[i+1] & 0x0F) << 2
                if i+2 > leng-1:
                    padded = True
                    third = carry
                else:
                    third = carry | ((plainint[i+2] & 0xC0) >> 6)
                third = B64.mapping[third]

            # Fourth
            if padded:
                fourth = "="
            else:
                fourth = plainint[i+2] & 0x3F
                fourth = B64.mapping[fourth]

            ciphertxt = ciphertxt + first + second + third + fourth 

        return ciphertxt

    def decode(ciphertxt: str) -> str:
        reverse_mapping = {v: k for k, v in B64.mapping.items()} 
        if len(ciphertxt) < 4 or len(ciphertxt) % 4 != 0:
            print("Invalid ciphertext! Needs to be a non-empty string with padding!")

        cipherlst = [char for char in ciphertxt]
        plaintxt = []
        for i in range(0, len(cipherlst), 4):
            # First
            first = reverse_mapping[cipherlst[i]] << 2 |\
                    reverse_mapping[cipherlst[i+1]] >> 4
            plaintxt.append(first)

            # Second
            if cipherlst[i+2] == '=': # Padding char
                break
            second = (reverse_mapping[cipherlst[i+1]] & 0x0F) << 4 |\
                     reverse_mapping[cipherlst[i+2]] >> 2
            plaintxt.append(second)

            # Third
            if cipherlst[i+3] == '=': # Padding char
                break
            third = (reverse_mapping[cipherlst[i+2]] & 0x03) << 6 |\
                    reverse_mapping[cipherlst[i+3]]
            plaintxt.append(third)
        
        plaintxt = bytes(plaintxt).decode()

        return plaintxt

def test_encode(plaintxt: str, chunk_size=3) -> str:
    mismatch_found = False
    my_encode = B64.encode(plaintxt)
    ext_encode = base64.b64encode(plaintxt.encode()).decode()
    while(len(my_encode) != len(ext_encode)):
        if len(my_encode) > len(ext_encode):
            ext_encode = ext_encode + '?'
        else:
            my_encode = my_encode + '?'

    for i in range(0, len(my_encode), chunk_size*4): # Because groups of 4 chars in B64 ciphertxt
        my_chunk = my_encode[i : i + chunk_size*4]
        ext_chunk = ext_encode[i : i + chunk_size*4]
        print(my_encode[i : i + chunk_size*4], "vs",
              ext_encode[i : i + chunk_size*4], end='')
        if my_chunk != ext_chunk:
            mismatch_found = True
            print(" <--- MISMATCH", my_chunk.encode().hex(), "vs",
                                    ext_chunk.encode().hex(), end='')
        print()

    if mismatch_found:
        print("Mismatch found")
    else:
        print("No mismatch found")
    print()

    return mismatch_found

def test_decode(ciphertxt: str, chunk_size=3) -> str:
    mismatch_found = False
    my_decode = B64.decode(ciphertxt)
    ext_decode = base64.b64decode(ciphertxt.encode()).decode()
    while(len(my_decode) != len(ext_decode)):
        if len(my_decode) > len(ext_decode):
            ext_decode = ext_decode + '?'
        else:
            my_decode = my_decode + '?'

    for i in range(0, len(my_decode), chunk_size*3): # Because groups of 3 chars in B64 plaintxt
        my_chunk = my_decode[i : i + chunk_size*3]
        ext_chunk = ext_decode[i : i + chunk_size*3]
        print(my_decode[i : i + chunk_size*3], "vs",
              ext_decode[i : i + chunk_size*3], end='')
        if my_chunk != ext_chunk:
            mismatch_found = True
            print(" <--- MISMATCH", my_chunk.encode().hex(), "vs",
                                    ext_chunk.encode().hex(), end='')
        print()

    if mismatch_found:
        print("Mismatch found")
    else:
        print("No mismatch found")
    print()

    return mismatch_found

if __name__ == "__main__":
    print('-'*90)

    print("Test encode")
    test_encode("Man")
    test_encode("Ma")
    test_encode("M")
    test_string = "Man is distinguished, not only by his reason, but by this singular passion from other animals, which is a lust of the mind, that by a perseverance of delight in the continued and indefatigable generation of knowledge, exceeds the short vehemence of any carnal pleasure."
    test_encode(test_string, chunk_size=9)

    print('-'*90)

    print("Test decode")
    test_decode("TWFu")
    test_decode("TWE=")
    test_decode("TQ==")
    test_decode(B64.encode(test_string), chunk_size=9)

    print('-'*90)
