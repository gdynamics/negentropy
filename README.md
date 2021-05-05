# Negentropy

*The concept and phrace "negative entropy" was introduced by Erwin Schrödinger in his 1944
popular-science book What is Life? Later, Léon Brillouin shortened the phrase to negentropy.*
([source](https://en.wikipedia.org/wiki/Negentropy))

In short, negentropy is the opposite of entropy.

## Current tools

### entropydiff-binwalk.py
This tool, given the paths of two files, will attempt to use binwalk through subprocess'ing
`binwalk -E {file}` to both files, and capture the values returned. It then prints out the entropy
of each individual file, and then the difference between them.

This allows you to compare the output of other negentropic tools to compare the original unaltered
English text's entropy to the files which are encrypted & obscured by the negentropic tools,
creating a baseline to measure the effectiveness of the method.

It is possible to compare the results to a larger, more general text as well, if you are simply
looking to compare to a more "global" baseline. However, comparing to the kind of data you are
going to be hiding in is the best method to measure utility.

### openssl-aes256.sh
A very, very simple Bash script. Simply pass it a filename, and it will create an encrypted version
of that file with the original filename with '.enc' at the end. The password it used to encrypt the
text is the all-too-secure password of "password", and the specific AES encryption method is
AES-256-CBC.

### b64.py & b64padless.py -> scripts/b64_encodefile.py

b64.py & b64padless.py are scripts which include B64 and B64padless MappedTranscoder classes
which can perform perform Base64 encoding and decoding. B64 performs normal Base64 encoding &
decoding, and B64Padless performs Base64 encoding & decoding without the need for padding.

The script b64_encodefile.py is a tool which uses B64 to encode a normal version and an encrypted
version of Macbeth, and write out their results to test/macbeth.txt.b64 & test/macbeth.txt.enc.b64.
There is no script for doing such with B64padless, as it did not seem necessary.

### english64.py -> scripts/english64_encodefile.py
english64.py is a script which includes an English64 MappedTranscoder class which can perform
Base64 encoding and decoding with a custom mapping functionality. Namely, instead of outputting
characters, it outputs words with spaces between them. The words are mapped from 00->63 against the
64 most common words in the english language according to 1-1000.txt.

The script english64_encodefile.py is a tool which uses English64 to encode a normal version and an
encrypted version of Macbeth, and write out their results to test/macbeth.txt.e64 and
test/macbeth.txt.enc.e64.

By expanding single characters to entire english words with spacing, the hope is to decrease the
apparent entropy to a level which mimics actual English text. This method, naturally, can expand
the size of the output data somewhere from 1 to 5 times the size of the original. However,
it appears to generate semi-successful results. Due to the fact that we have a small bank of words
that are all short, very common, and very simple to pronounce, the entropy of the out is actually
relatively significantly lower than normal English text.

## Use cases

### Information hiding
In the cat and mouse game that is security, you have malware analysts & malware authors, corporate
software engineers & reverse engineers, etc. Malware authors and corporate software engineers alike
try to hide and secure their operations with encryption & encoding.

Some encryption & encoding methods like xor encryption and base64 encoding do not increase entropy,
but these methods are far less secure, and malware analysts & general reverse engineers are often
extremely familiar with these methods of hiding & safeguarding information, and are more than
capable of decrypting your hidden data, especially if you attempt to "roll your own crypto".

Other encryption methods such as AES are in almost every case significantly more secure than xor
encryption or base64 encoding, especially when implemented by professionals. However, these
encryption methods invariably add entropy to the system.

Unfortunately for malware authors and corporate software engineers, malware analysts & general
reverse engineers are just as familiar with the usage of these encryption methods. As a result,
it is common for both those
[analyzing malware](https://securelist.com/looking-for-sophisticated-malware-in-iot-devices/98530/)
and those
[reverse engineering firmware](https://www.refirmlabs.com/reverse-engineering-my-routers-firmware-with-binwalk/)
to use tools like `binwalk` to discover encrypted data. As a result, this leaks information of a kind
to them about where data is, allowing them to carve it out and search for assembly & APIs which
reference this data or encryption in general in an attempt to allow the product to self decrypt
so they can capture a dump or search for decryption keys to decrypt the data themselves.

By expanding the existing data to take up more space than it needs to, and converting truly random
data into things which are nonrandom, such as words, we can decrease the entropy of the data to the
eyes of tools such as binwalk.

As a result, it may be possible to defeat both simple information gathering methods (such as
binwalk's entropy measurement) and simple system & network security services & tools which search
for encrypted data.

## Warning

### This is research, not gospel
This tool is a bit of independent research I undertook on my own, simply to see if I can trick
binwalk and perhaps other entropy measuring tools into not seeing my secrets. I learned the entropy
measurement trick from firmware analysis tutorials a few years ago, and simply had an idea one day
on whether I could decrease entropy in a way that preserved the security of the encrypted data.

This work is not "professional." The software itself has not been audited, the tools' capacities
have not been checked by people with significant security experience for effectiveness, etc. I am
a Master's student with a small amount of work experience.

The tools & methods enclosed currently would be better fit for a CTF than a serious piece of
software of any kind, whether malicious, corporate, or both.

### Security through obscurity
At the end of the day, this tooling & research can be explained away as security by obscurity.
Many, myself included, believe that security through obscurity is not a proper answer to many, if
not all security problems.

However, if your goal is only to slow down beginner to intermediate reverse engineers or bypass a
"dumb," automated security tool such as an old fashioned file scanning antimalware service reading
your binary or memory, then this security through obscurity is a successful hack to increase your
chances of success.

I, personally, would say that malware authors benefit the most from this. If you are a corporate
software engineer building something such as an IoT device, you will have exponentially more to
gain from learning proper cryptographic principles, trust models, hardware security methodologies,
etc than from trying to implement this tool in your deployment.

tl;dr: This tool is more of a sleight at uncreative, untrained eyes than a security model unto
itself. It is meant to trick tools and fools, not experts.
