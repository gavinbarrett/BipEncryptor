#!/usr/bin/env python
import sys
from base64 import b64encode, b64decode
from validation import valid_passphrase, valid_mnemonic, valid_ciphermnemonic
from encryption import encrypt, decrypt, encrypt_mnemonic, decrypt_mnemonic

yellow = '\u001b[33m'
end = '\033[0m'

def parse_ciphermnemonic(ciphermnemonic):
	''' Parse the serialized ciphermnemonic <ciphertext.tag.nonce>'''
	try:
		parsed = [b64decode(x) for x in ciphermnemonic.split('.')]
		if (len(parsed) != 3):
			raise ValueError('Insufficient ciphermnemonic arguments.')
		return parsed
	except Exception as e:
		print(e)

def interpret_args(args):
	''' Run a valid command (encryption/decryption) '''
	if args[0] == '-e' and args[2] == '-k' and valid_passphrase(args[3]):
		if valid_mnemonic(args[1]):
			if valid_passphrase(args[3]):
				ciphermnemonic = encrypt_mnemonic(args[1], args[3].encode())
				print(f'Your ciphermnemonic is:\n{yellow}{ciphermnemonic}{end}')
			else:
				raise ValueError(f'Invalid passphrase: {args[3]}\nPassphrase must be between 10 and 64 characters [a-zA-Z0-9!@#$%&+=?]')
		else:
			raise ValueError(f'Invalid BIP mnemonics: {args[1]}')
		# FIXME: enforce that second argument is a single string that is BIP32 compatible
	elif args[0] == '-d' and args[2] == '-k':
		if valid_ciphermnemonic(args[1]) and valid_passphrase(args[3]):
			mnemonic = decrypt_mnemonic(args[1], args[3].encode())
			input("Phrase successfully decrypted. Press any key to reveal.")
			print(f'{yellow}{mnemonic.decode()}{end}')
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

def help():
	''' Print the functions command page '''
	print('Valid arguments: -e, -d, -h')


if __name__ == "__main__":
	parse_args(sys.argv)
