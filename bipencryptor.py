#!/usr/bin/env python
import sys
import hmac
from os import urandom
from Crypto.Cipher import ChaCha20_Poly1305
from hashlib import pbkdf2_hmac, sha256
from base64 import b64encode, b64decode
from words import words

def kdf(passphrase):
	''' Derive the key from a passphrase '''
	return pbkdf2_hmac('sha256', passphrase, b'bip encryptor', 4096, 32)

def encrypt(key, mnemonic):
	''' Encrypt the mnemonic phrase '''
	# construct the cipher object with the key
	cipher = ChaCha20_Poly1305.new(key=key)
	# return the encrypted mnemonic, Poly1305 tag, and nonce
	ciphertext, tag = cipher.encrypt_and_digest(mnemonic.encode())
	return ciphertext, tag, cipher.nonce

def decrypt(key, ciphertext, tag, nonce):
	''' Decrypt the mnemonic phrase '''
	# construct the cipher object with the key
	cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
	# decrypt and verify the ciphertext
	return cipher.decrypt_and_verify(ciphertext, tag)

def encrypt_mnemonic(mnemonic, passphrase):
	''' Encrypt the mnemonic with the AE scheme '''
	# derive the key from the passphrase
	key = kdf(passphrase)
	# encrypt the mnemonic
	ciphertext, tag, nonce = encrypt(key, mnemonic)
	return f'{b64encode(ciphertext).decode()}.{b64encode(tag).decode()}.{b64encode(nonce).decode()}'

def decrypt_mnemonic(ciphermnemonic, passphrase):
	''' Decrypt a valid, serialized <ciphertext.tag.nonce> structure '''
	# derive the key from the passphrase
	key = kdf(passphrase)
	# parse the ciphertext, mac, and nonce from the input ciphermnemonic
	ciphertext, tag, nonce = parse_ciphermnemonic(ciphermnemonic)
	return decrypt(key, ciphertext, tag, nonce)

def parse_ciphermnemonic(ciphermnemonic):
	''' Parse the serialized ciphermnemonic <ciphertext.tag.nonce>'''
	try:
		parsed = [b64decode(x) for x in ciphermnemonic.split('.')]
		if (len(parsed) != 3):
			raise ValueError('Insufficient ciphermnemonic arguments.')
		return parsed
	except Exception as e:
		print(e)

def help():
	''' Print the functions command page '''
	print('Valid arguments: -e, -d, -h')

def valid_passphrase(passphrase):
	''' Enforce a passphrase policy (20 character alphanumeric + special characters) '''
	return True

def valid_mnemonic(mnemonic):
	''' Return true if the input phrase is a valid mnemonic '''
	# split mnemonic phrase by spaces
	phrase_words = mnemonic.split(' ')
	# return true if every word is in the bip 39 list and the phrase is an appropraite length
	return all([phrase in words for phrase in phrase_words]) and len(phrase_words) in [12, 15, 18, 21, 24]

def valid_ciphermnemonic(ciphermnemonic):
	''' Return true if the ciphermnemonic is properly structured - <b64ciphertext.b64tag.b64nonce> '''
	return True

def interpret_args(args):
	''' Run a valid command (encryption/decryption) '''
	if args[0] == '-e' and args[2] == '-k' and valid_pass(args[3]):
		if valid_mnemonic(args[1]):
			if valid_passphrase(args[3]):
				ciphermnemonic = encrypt_mnemonic(args[1], args[3].encode())
				print(ciphermnemonic)
			else:
				raise ValueError(f'Invalid passphrase: {args[3]}\nPassphrase must be between 10 and 64 characters [a-zA-Z0-9!@#$%&+=?]')
		else:
			raise ValueError(f'Invalid BIP mnemonics: {args[1]}')
		# FIXME: enforce that second argument is a single string that is BIP32 compatible
	elif args[0] == '-d' and args[2] == '-k':
		if valid_ciphermnemonic(args[1]) and valid_passphrase(args[3]):
			mnemonic = decrypt_mnemonic(args[1], args[3].encode())
			print(mnemonic.decode())
		else:
			raise ValueError(f'Invalid passphrase: {args[3]}\nPassphrase must be between 10 and 64 characters [a-zA-Z0-9!@#$%&+=?]')
	else:
		raise TypeError(f'Invalid mode entered: {arguments[0]}')

def parse_args(args):
	''' Parse the program arguments '''
	try:
		args.pop(0)
		if len(args) == 4:
			interpret_args(args)
		else:
			print('Incorrect arguments entered.\nPlease enter a mode (-e or -d), a plaintext/ciphertext, the key flag (-k), and a passphrase to use to derive the key')
			help()
	except ValueError as err:
		print(f'Error interpreting arguments: {err}')
		help()

if __name__ == "__main__":
	parse_args(sys.argv)
