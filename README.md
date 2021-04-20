### BipEncryptor
BipEncryptor is a simple authenticated encryption scheme for securing BIP32/39 cryptocurrency recovery phrases.

```bash
$ ./bipencryptor -e "hospital blanket pottery close sheriff gate agree vintage truly antique arm radar" -k "th15is@secr3tp@ssphr@senob0dykn0wsbutm3"

$ ZwxKFJ7N/Be4ssWBWs0HAd6cvqOKEn1mDKN1+Gnh+pIskTE6rw3YXK1GIju88RhqtZfIGi/Nr5bBbsGepRhATCzjrSz1KLGedNOpmL8BKxTb;lsAGRJRnPuqEms4KHVKh/A==;sutuJRTEQan1l1co
```


```bash
$ ./bipencryptor -d "ZwxKFJ7N/Be4ssWBWs0HAd6cvqOKEn1mDKN1+Gnh+pIskTE6rw3YXK1GIju88RhqtZfIGi/Nr5bBbsGepRhATCzjrSz1KLGedNOpmL8BKxTb;lsAGRJRnPuqEms4KHVKh/A==;sutuJRTEQan1l1co" -k "th15is@secr3tp@ssphr@senob0dykn0wsbutm3"

$ hospital blanket pottery close sheriff gate agree vintage truly antique arm radar
```
