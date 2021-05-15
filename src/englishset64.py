#!/usr/bin/env python
from mappedtranscoder import MappedTranscoder
import random

class EnglishSet64(MappedTranscoder):
    def generate_mapping(filename: str) -> dict:
        mapping = {}

        with open(filename, 'r') as mapping_file:
            data = mapping_file.read()

        data = data.split()

        for i in range(0,64):
            mapping[i] = []

        for i in range(0, len(data)):
            mapping[i%64].append(data[i])

        return mapping

    def encode(plaintxt: bytes) -> str:
        mapping = EnglishSet64.generate_mapping('1-1000.txt')
        ciphertxt = None
        leng = len(plaintxt)

        for i in range(0, len(plaintxt), 3):
            end = False
            
            # First
            first = (plaintxt[i] & 0xFD) >> 2
            first = random.choice(mapping[first])

            # Second
            carry = (plaintxt[i] & 0x03) << 4
            if i+1 > leng-1:
                end = True
                second = carry
            else:
                second = carry | ((plaintxt[i+1] & 0xF0) >> 4)
            second = random.choice(mapping[second])

            # Third
            if end:
                third = ""
            else:
                carry = (plaintxt[i+1] & 0x0F) << 2
                if i+2 > leng-1:
                    end = True
                    third = carry
                else:
                    third = carry | ((plaintxt[i+2] & 0xC0) >> 6)
                third = random.choice(mapping[third])

            # Fourth
            if end:
                fourth = ""
            else:
                fourth = plaintxt[i+2] & 0x3F
                fourth = random.choice(mapping[fourth])

            ciphertxt = ' '.join([ciphertxt, first, second, third, fourth] if ciphertxt
                            else [first, second, third, fourth])

        return ciphertxt

    def decode(ciphertxt: str) -> bytes:
        mapping = EnglishSet64.generate_mapping('1-1000.txt')
        reverse_mapping = {v: k for k, v in mapping.items()}
        ciphertxt = ciphertxt.split()
        cipher_len = len(ciphertxt)
        if cipher_len < 2:
            print("Invalid ciphertext! Needs to be a non-empty string with at least 2 characters!")

        cipherlst = [word for word in ciphertxt]
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

        plaintxt = bytes(plaintxt)

        return plaintxt

if __name__ == "__main__":
    print('-'*90)

    print("Test encode")
    print(EnglishSet64.encode(b"Man"))
    print(EnglishSet64.encode(b"Ma"))
    print(EnglishSet64.encode(b"M"))
    test_string = b"Man is distinguished, not only by his reason, but by this singular passion from other animals, which is a lust of the mind, that by a perseverance of delight in the continued and indefatigable generation of knowledge, exceeds the short vehemence of any carnal pleasure."
    print(EnglishSet64.encode(test_string))

    print('-'*90)

    #print("Test decode")
    #print(English64.decode("they one in said"))
    #print(English64.decode("they one a"))
    #print(English64.decode("they as"))
    #print(English64.decode("they one in said you is other do you is I when by will I when had were not time or have on there from one as your you is about an not to of an had were she about you is that about you is some when by which of which from one in do had if way your you is that time not to of we word his of their or is other do you it on when had were not time had is in which you it of some by will on when had if way what from all that an had his of an not is some other by we of some had were other how this one she do was to of will or is other can or to of when by which of some you is she time by will as what had if this what not is some other you is time when had were as your you it I there this have as what this all out what this his of each from have that do from have from other by were in said this if be what had if this what from is at your or one not there not to of when had we of their or is be what this if write said not is other said not one at out you is in said from to of when had were I other from were in their or one not some this were she other you is not other had were at which this have I when had if way what had if this what or if about an not if she other from is not other was to of other word is on other from one I do you it I there from his of do or is write which not to of if from one some other had one at said this if be what had if this what this one about about you is on some by were about some had to of each had is at some by will at which from his way"))

    #print('-'*90)
