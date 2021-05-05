#!/usr/bin/env python
import os, sys

sys.path.append(os.path.abspath('../'))
import b64

if __name__ == "__main__":
    print('-'*90)

    print("Test encode")
    b64.test_encode("Man")
    b64.test_encode("Ma")
    b64.test_encode("M")
    test_string = "Man is distinguished, not only by his reason, but by this singular passion from other animals, which is a lust of the mind, that by a perseverance of delight in the continued and indefatigable generation of knowledge, exceeds the short vehemence of any carnal pleasure."
    b64.test_encode(test_string, chunk_size=9)

    print('-'*90)
