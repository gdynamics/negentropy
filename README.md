# Negentropy

_The concept and phrase "negative entropy" was introduced by Erwin Schrödinger in his 1944
popular-science book What is Life? Later, Léon Brillouin shortened the phrase to negentropy._
([source](https://en.wikipedia.org/wiki/Negentropy))

In short, negentropy is the opposite of entropy.

## Current tools

### entropydiff_binwalk.py
This tool, given the paths of two files, will attempt to use `binwalk` through subprocess'ing
`binwalk -E {file}` to both files, and capture the values returned. It then prints out the entropy
of each individual file, and then the difference between them.

This allows you to compare the output of other negentropic tools to compare the original unaltered
English text's entropy to the files which are encrypted & obscured by the negentropic tools,
creating a baseline to measure the effectiveness of the method.

It is possible to compare the results to a larger, more general text as well, if you are simply
looking to compare to a more "global" baseline. However, comparing to the kind of data you are
going to be hiding in is the best method to measure utility.

Example usage, comparing the variance between normal macbeth and an encrypted macbeth hidden with
`EnglishSet64.py`, utilizing `1-1000.txt` as its key file:
```
.../negentropy$ ./src/scripts/entropydiff_binwalk.py ./src/test/macbeth.txt ./src/test/macbeth.txt.enc.2.es64

--------------------------------------------------
./src/test/macbeth.txt            : 0.648474
./src/test/macbeth.txt.enc.2.es64 : 0.5141
                                   ----------
Difference                        : 0.134374
-------------------------------------------------- 
```

### openssl_aes256.sh
A very, very simple Bash script. Simply pass it a filename, and it will create an encrypted version
of that file with the original filename with **'.enc'** at the end. The password it used to encrypt the
text is the all-too-secure password of **"password"**, and the specific AES encryption method is
**AES-256-CBC**.

### b64.py & b64padless.py -> scripts/b64_encodefile.py

`b64.py` & `b64padless.py` are scripts which include `B64` and `B64padless` `MappedTranscoder` classes
which can perform perform Base64 encoding and decoding. `B64` performs normal Base64 encoding &
decoding, and `B64Padless` performs Base64 encoding & decoding without the need for padding.

The script `b64_encodefile.py` is a tool which uses `B64` to encode a normal version and an encrypted
version of Macbeth, and write out their results to `test/macbeth.txt.b64` & `test/macbeth.txt.enc.b64`.
There is no script for doing such with `B64padless`, as it did not seem necessary.

### english64.py -> scripts/english64_encodefile.py
`english64.py` is a script which includes an `English64` `MappedTranscoder` class which can perform
Base64 encoding and decoding with a custom mapping functionality. Namely, instead of outputting
characters, it outputs words with spaces between them. The words are mapped from **0->63** against the
64 most common words in the english language according to `1-1000.txt`.

The script `english64_encodefile.py` is a tool which uses `English64` to encode a normal version and an
encrypted version of Macbeth, and write out their results to `test/macbeth.txt.e64` and
`test/macbeth.txt.enc.e64`.

By expanding single characters to entire english words with spacing, the hope is to decrease the
apparent entropy to a level which mimics actual English text. This method, naturally, can expand
the size of the output data somewhere from 1 to 5 times the size of the original. However,
it appears to generate semi-successful results. Due to the fact that we have a small bank of words
that are all short, very common, and very simple to pronounce, the entropy of the out is actually
relatively significantly lower than normal English text.

### englishset64.py -> scripts/englishset64_encodefile.py
`englishset64.py` is a script which includes an `EnglishSet64` `MappedTranscoder` class which can
perform Base64 encoding and decoding with a custom mapping functionality. In a stark contrast to
`english64.py`, this script will generate a mapping to all of the words (text separated by
whitespace) in its key file. This means firstly that 0:63 map to a list of words rather than to one
single word each. This makes encoding slightly slower, and decoding much slower, as decoding has to
perform a O(n^2) search for the corresponding index to a given word in the key, rather than simply
using the reverse mapping trick used to get O(1) through dicts in b64, english64, etc. An important
implementation detail is that the methodology for choosing a word out of the list corresponding to
an index is done randomly, through Python's `random.choice()` functionality.

The script `englishset64_encodefile.py` is a tool which uses `EnglishSet64` to encode a plaintext
version and an encrypted version of Macbeth, and write out their results to
`test/macbeth.txt.es64`, `test/macbeth.txt.enc.1.es64`, and `test/macbeth.txt.enc.2.es64`.

Identically to `English64`, by expanding single characters to entire english words with spacing, the
hope is to decrease the apparent entropy to a level which mimics actual English text. This method,
naturally, can expand the size of the output data. However, as opposed to `English64`, `EnglishSet64`
generates text that is 1 to the size of the largest word in your key file of the original. By
utilizing a large list of words per index rather than a single word, attacks which attempt to
detect the information hiding and reverse it by frequency analysis of words, as well as attempts
which simply discover that there are 64 unique words are rendered useless. Also, by utilizing a key
file, you can dynamically tune your entropy to better match the kind of text you intend to imitate.
An approach with a custom key file may do something as simple as a Bash script where a text file is
cleaned of all special characters, split into newlines, and run through the `uniq` utility.
Finally, through the implementation of `random.choice`, no given input and key file will be likely
to generate identical or particularly similar results, making an attack that re-encodes its
hidden data per-copy to new system not discoverable and easily rooted out through searching for a
single identical ciphertext, and each generated ciphertext has a slightly different entropy.
 
It is important to note for anyone attempting to generate their own key file, however, that each
word in the key file must be unique and never repeated, as otherwise you would incorrectly decode
the word to the first index which has that word, rather than the original number, which may
correspond to the 2nd or later index with that word.

As for its success, `EnglishSet64` does its job as described. It, unsurprisingly, has an entropy
closer to the cleartext than `English64` does, most obviously because they share the same source,
`1-1000.txt` in their current implementations, and `EnglishSet64` utilizes all 1000 words rather
than just the 64 most common, giving it a wider variety of characters, word lengths, etc. The best
way I can think of detecting if someone is using this approach in multiple places from data alone
appears to be that the entropies of all ciphertexts with the same key and input will likely be
within a specific range of each other. More complex detection methodologies like searching for
batches of text with a lot of the words in a known key file or words from a previous ciphertext
may be possible. Most obviously, however, is just that the english is pretty much just as
nonsensical, unpunctuated, and uncapitalized as `English64`, making actual well trained analysis
show something is "up" very quickly.


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
eyes of tools such as `binwalk`.

As a result, it may be possible to defeat both simple information gathering methods (such as
`binwalk`'s entropy measurement) and simple system & network security services & tools which search
for encrypted data.

## Warning

### This is research, not gospel
This tool is a bit of independent research I undertook on my own, simply to see if I can trick
`binwalk` and perhaps other entropy measuring tools into not seeing my secrets. I learned the entropy
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

**tl;dr: This tool is more of a sleight at uncreative, untrained eyes than a security model unto
itself. It is meant to trick tools and fools, not experts.**
