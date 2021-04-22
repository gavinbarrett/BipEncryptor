from hashlib import pbkdf2_hmac

def kdf(passphrase):
	''' Derive the key from a passphrase '''
	return pbkdf2_hmac('sha256', passphrase, b'bip encryptor', 4096, 32)
