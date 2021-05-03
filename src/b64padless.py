#!/usr/bin/env python
from mappedtranscoder import MappedTranscoder
import base64 # Just for testing

class B64padless(MappedTranscoder):
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
            end = False
            
            # First
            first = (plainint[i] & 0xFD) >> 2
            first = B64padless.mapping[first]

            # Second
            carry = (plainint[i] & 0x03) << 4
            if i+1 > leng-1:
                end = True
                second = carry
            else:
                second = carry | ((plainint[i+1] & 0xF0) >> 4)
            second = B64padless.mapping[second]

            # Third
            if end:
                third = ""
            else:
                carry = (plainint[i+1] & 0x0F) << 2
                if i+2 > leng-1:
                    end = True
                    third = carry
                else:
                    third = carry | ((plainint[i+2] & 0xC0) >> 6)
                third = B64padless.mapping[third]

            # Fourth
            if end:
                fourth = ""
            else:
                fourth = plainint[i+2] & 0x3F
                fourth = B64padless.mapping[fourth]

            ciphertxt = ciphertxt + first + second + third + fourth 

        return ciphertxt

    def decode(ciphertxt: str) -> str:
        reverse_mapping = {v: k for k, v in B64padless.mapping.items()} 
        cipher_len = len(ciphertxt)
        if cipher_len < 1:
            print("Invalid ciphertext! Needs to be a non-empty string!")

        cipherlst = [char for char in ciphertxt]
        plaintxt = []
        for i in range(0, len(cipherlst), 4):
            # First
            first = reverse_mapping[cipherlst[i]] << 2 |\
                    reverse_mapping[cipherlst[i+1]] >> 4
            plaintxt.append(first)

            # Second
            if i+2 >= cipher_len: # Reached end
                break
            second = (reverse_mapping[cipherlst[i+1]] & 0x0F) << 4 |\
                     reverse_mapping[cipherlst[i+2]] >> 2
            plaintxt.append(second)

            # Third
            if i+3 >= cipher_len: # Reached end
                break
            third = (reverse_mapping[cipherlst[i+2]] & 0x03) << 6 |\
                    reverse_mapping[cipherlst[i+3]]
            plaintxt.append(third)
        
        plaintxt = bytes(plaintxt).decode()

        return plaintxt

def test_encode(plaintxt: str, chunk_size=3) -> str:
    mismatch_found = False
    my_encode = B64padless.encode(plaintxt)
    ext_encode = base64.b64encode(plaintxt.encode()).decode()
    ext_encode = ext_encode.replace('=', '') # Remove padding
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
    padded_ciphertxt = ciphertxt + '='*((4-(len(ciphertxt)+4))%4)
    my_decode = B64padless.decode(ciphertxt)
    ext_decode = base64.b64decode(padded_ciphertxt.encode()).decode()
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
    test_decode("TWE")
    test_decode("TQ")
    test_decode(B64padless.encode(test_string), chunk_size=9)

    print('-'*90)
