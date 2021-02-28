#!/bin/bash

if [[ $# -ne 1 ]]; then
	echo "Filename, please"
	exit 1
fi

# Encrypt input file with AES, 256 bit, CBC mode, with the password "password"
openssl enc -aes-256-cbc -in "$1" -out "$1.enc" -pass pass:password

exit 0
