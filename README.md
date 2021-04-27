## Description
BipEncryptor is an [authenticated encryption](https://en.wikipedia.org/wiki/Authenticated_encryption) scheme for securing BIP32/39 cryptocurrency recovery phrases. Upon encrypting, the program will produce a serialized string composed of four base64-encoded values, separated by a period:
```
<ciphertext.mac.nonce.kdf_args>
```

The period-separated values are as follows:

1. The ciphertext obtained by encrypting the mnemonic phrase with ChaCha20
2. The MAC obtained through authenticating with Poly1305
3. The nonce value used with the ChaCha20 cipher
4. A semi-colon-separated list of arguments for the argon2 key derivation function

Before being encoded with base64, the last value looks something like this:
```
16;1183492;8
```

And refers to the following argon2 parameters:
1. The time cost argument
2. The memory argument in bytes
3. The number of virtual CPU cores of the client computer

### Cryptographic Primitives
This project is written in Python and uses the ```pycryptodome``` implementation of ChaCha20-Poly1305 for encryption and authentication. It uses the ```argon2-cffi``` package


### Encryption

```bash
$ ./bipencryptor.py -e "hospital blanket pottery close sheriff gate agree vintage truly antique arm radar" -k "th15is@secr3tp@ssphr@senob0dykn0wsbutm3"

$ ZwxKFJ7N/Be4ssWBWs0HAd6cvqOKEn1mDKN1+Gnh+pIskTE6rw3YXK1GIju88RhqtZfIGi/Nr5bBbsGepRhATCzjrSz1KLGedNOpmL8BKxTb;lsAGRJRnPuqEms4KHVKh/A==;sutuJRTEQan1l1co
```


### Decryption

```bash
$ ./bipencryptor.py -d "ZwxKFJ7N/Be4ssWBWs0HAd6cvqOKEn1mDKN1+Gnh+pIskTE6rw3YXK1GIju88RhqtZfIGi/Nr5bBbsGepRhATCzjrSz1KLGedNOpmL8BKxTb;lsAGRJRnPuqEms4KHVKh/A==;sutuJRTEQan1l1co" -k "th15is@secr3tp@ssphr@senob0dykn0wsbutm3"

$ hospital blanket pottery close sheriff gate agree vintage truly antique arm radar
```


### Disclaimer
Do not send funds to any cryptocurrency address associated with the aforementioned mnemonic phrase, or they will be taken.
