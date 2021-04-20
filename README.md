## Description
BipEncryptor is an [authenticated encryption](https://en.wikipedia.org/wiki/Authenticated_encryption) scheme for securing BIP32/39 cryptocurrency recovery phrases.


### Encryption

```bash
$ ./bipencryptor -e "hospital blanket pottery close sheriff gate agree vintage truly antique arm radar" -k "th15is@secr3tp@ssphr@senob0dykn0wsbutm3"

$ ZwxKFJ7N/Be4ssWBWs0HAd6cvqOKEn1mDKN1+Gnh+pIskTE6rw3YXK1GIju88RhqtZfIGi/Nr5bBbsGepRhATCzjrSz1KLGedNOpmL8BKxTb;lsAGRJRnPuqEms4KHVKh/A==;sutuJRTEQan1l1co
```


### Decryption

```bash
$ ./bipencryptor -d "ZwxKFJ7N/Be4ssWBWs0HAd6cvqOKEn1mDKN1+Gnh+pIskTE6rw3YXK1GIju88RhqtZfIGi/Nr5bBbsGepRhATCzjrSz1KLGedNOpmL8BKxTb;lsAGRJRnPuqEms4KHVKh/A==;sutuJRTEQan1l1co" -k "th15is@secr3tp@ssphr@senob0dykn0wsbutm3"

$ hospital blanket pottery close sheriff gate agree vintage truly antique arm radar
```
