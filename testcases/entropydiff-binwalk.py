#!/usr/bin/python3

import sys
import subprocess

def binwalk_entropy(file):
    cmd = f"binwalk -E {file}"
    raw = str(subprocess.check_output(cmd, shell=True))
    value = float(raw[raw.find('(')+1 : raw.find(')')])
    return value

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Two files, please")
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    file1_ent = binwalk_entropy(file1)
    file2_ent = binwalk_entropy(file2)

    difference = max(file1_ent, file2_ent) - min(file1_ent, file2_ent)

    size = max(len(file1), len(file2))
    print(f"{file1.ljust(size)} : {file1_ent}")
    print(f"{file2.ljust(size)} : {file2_ent}")
    print('-'*30)
    print("Difference".ljust(size), ':', difference)

