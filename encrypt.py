import sys
import hmac
from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import pbkdf2_hmac, sha256
from base64 import b64encode
from words import words

def kdf(passphrase):
	''' Derive the key from as passphrase '''
	return pbkdf2_hmac('sha256', passphrase.encode(), b'bip encryptor', 2048, 32)

def encrypt(key, mnemonic):
	''' Encrypt the mnemonic phrase '''
	iv = urandom(16)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return cipher.encrypt(pad(mnemonic.encode(), AES.block_size))

def decrypt(key, ciphermnemonic):
	''' Decrypt the mnemonic phrase '''
	pass	

def auth():
	pass

def encrypt_mnemonic(mnemonic, passphrase):
	''' Encrypt the mnemonic with the AE scheme '''
	key = kdf(passphrase)
	ciphertext = encrypt(key, mnemonic)
	print(f'Ciphertext: {b64encode(ciphertext)}')

def decrypt_mnemonic(ciphermnemonic, passphrase):
	key = kdf(passphrase)
	mnemonic = decrypt(key, ciphermnemonic)
	print(f'Mnemonic: {mnemonic}')

def help():
	''' Print the functions command page '''
	print('Valid arguments: -e, -d, -h')

def valid_pass(passphrase):
	''' Return true if the input phrase is a valid passphrase '''
	return True

def valid_mnemonic(mnemonic):
	''' Return true if the input phrase is a valid mnemonic '''
	# split mnemonic phrase by spaces
	phrase_words = mnemonic.split(' ')
	# return true if every word is in the bip 39 list and the phrase is an appropraite length
	return all([phrase in words for phrase in phrase_words]) and len(phrase_words) in [12, 15, 18, 21, 24]

def interpret_args(args):
	if args[0] == '-e' and args[2] == '-k' and valid_pass(args[3]):
		if valid_mnemonic(args[1]):
			if valid_pass(args[3]):
				encrypt_mnemonic(args[1], args[3])
			else:
				raise ValueError(f'Invalid passphrase: {args[3]}\nPassphrase must be between 10 and 64 characters [a-zA-Z0-9!@#$%&+=?]')
		else:
			raise ValueError(f'Invalid BIP mnemonics: {args[1]}')
		# FIXME: enforce that second argument is a single string that is BIP32 compatible
	elif args[0] == '-d' and args[2] == '-k':
		if valid_mnemonic(args[1]):
			if valid_pass(args[3]):
				decrypt_mnemonic(args[1], args[3])
			else:
				raise ValueError(f'Invalid passphrase: {args[3]}\nPassphrase must be between 10 and 64 characters [a-zA-Z0-9!@#$%&+=?]')
		else:
			raise ValueError(f'Invalid BIP mnemonics: {args[1]}')
	else:
		raise TypeError(f'Invalid mode entered: {arguments[0]}')

if __name__ == "__main__":
	args = sys.argv
	args.pop(0)
	try:
		if len(args) == 4:
			interpret_args(args)
		else:
			print('Incorrect arguments entered.\nPlease enter a mode (-e or -d), a plaintext/ciphertext, the key flag (-k), and a passphrase to use to derive the key')
			help()
	except ValueError as err:
		print(f'Error interpreting arguments: {err}')
		help()
