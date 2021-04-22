from base64 import b64encode, b64decode
from Crypto.Cipher import ChaCha20_Poly1305
from keystretch import kdf

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
