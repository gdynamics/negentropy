#!/usr/bin/env python
from mappedtranscoder import MappedTranscoder
import base64 # Just for testing

class B64(MappedTranscoder):
    mapping = {
             0: 'A',  1: 'B',  2: 'C',  3: 'D',
             4: 'E',  5: 'F',  6: 'G',  7: 'H',
             8: 'I',  9: 'J', 10: 'K', 11: 'L',
            12: 'M', 13: 'N', 14: 'O', 15: 'P',
            16: 'Q', 17: 'R', 18: 'S', 19: 'T',
            20: 'U', 21: 'V', 22: 'W', 23: 'X',
            24: 'Y', 25: 'Z', 26: 'a', 27: 'b',
            28: 'c', 29: 'd', 30: 'e', 31: 'f',
            32: 'g', 33: 'h', 34: 'i', 35: 'j',
            36: 'k', 37: 'l', 38: 'm', 39: 'n',
            40: 'o', 41: 'p', 42: 'q', 43: 'r',
            44: 's', 45: 't', 46: 'u', 47: 'v',
            48: 'w', 49: 'x', 50: 'y', 51: 'z',
            52: '0', 53: '1', 54: '2', 55: '3',
            56: '4', 57: '5', 58: '6', 59: '7',
            60: '8', 61: '9', 62: '+', 63: '/',
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
            print([i for i in cipherlst[i:i+4]])
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

        print(plaintxt)
        return "decode"

def test_encode(plaintxt: str, chunk_size=3) -> str:
    mismatch_found = False
    my_encode = B64.encode(plaintxt).upper()
    ext_encode = base64.b64encode(plaintxt.encode()).decode().upper()
    while(len(my_encode) != len(ext_encode)):
        if len(my_encode) > len(ext_encode):
            ext_encode = ext_encode + '?'
        else:
            my_encode = my_encode + '?'

    for i in range(0, len(my_encode), chunk_size*4): # Because groups of 4 chars in B64, *3
        my_chunk = my_encode[i : i + chunk_size*4]
        ext_chunk = ext_encode[i : i + chunk_size*4]
        print(my_encode[i : i + chunk_size*4], "vs",
              ext_encode[i : i + chunk_size*4], end='')
        if my_chunk != ext_chunk:
            mismatch_found = True
            print(" <--- MISMATCH", my_chunk.encode().hex().upper(), "vs",
                                    ext_chunk.encode().hex().upper(), end='')
        print()

    if mismatch_found:
        print("Mismatch found")
    else:
        print("No mismatch found")
    print()

    return mismatch_found

if __name__ == "__main__":
    test_encode("Man")
    test_encode("Ma")
    test_encode("M")
    test_string = "Man is distinguished, not only by his reason, but by this singular passion from other animals, which is a lust of the mind, that by a perseverance of delight in the continued and indefatigable generation of knowledge, exceeds the short vehemence of any carnal pleasure."
    test_encode(test_string, chunk_size=9)

    B64.decode("TWFU")
    B64.decode("TWE=")
    B64.decode("TQ==")
