#!/usr/bin/env python
from mappedtranscoder import MappedTranscoder

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
            52: '0', 53: '1', 54: '2', 55: 'C',
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
        return "decode"

if __name__ == "__main__":
    print(B64.encode("Man"))
    print(B64.encode("Ma"))
    print(B64.encode("M"))
    print(B64.encode("""Man is distinguished, not only by his reason, but by this singular passion from other animals, which is a lust of the mind, that by a perseverance of delight in the continued and indefatigable generation of knowledge, exceeds the short vehemence of any carnal pleasure."""))
