from base64 import b64encode, b64decode
from Crypto.Cipher import ChaCha20_Poly1305
from keystretch import kdf, kdf_decrypt

red = '\u001b[31m'
green = '\u001b[32m'
end = '\033[0m'

def encrypt(key, mnemonic):
	''' Encrypt the mnemonic phrase '''
	# construct the cipher object with the key
	cipher = ChaCha20_Poly1305.new(key=key)
	print(f'{green}Encrypting mnemonic phrase.{end}')
	# return the encrypted mnemonic, Poly1305 tag, and nonce
	ciphertext, tag = cipher.encrypt_and_digest(mnemonic.encode())
	return ciphertext, tag, cipher.nonce

def decrypt(key, ciphertext, tag, nonce):
	''' Decrypt the mnemonic phrase '''
	# construct the cipher object with the key
	cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
	print(f'{red}Decrypting mnemonic phrase.{end}')
	# decrypt and verify the ciphertext
	return cipher.decrypt_and_verify(ciphertext, tag)

def encrypt_mnemonic(mnemonic, passphrase):
	''' Encrypt the mnemonic with the AE scheme '''
	# derive the key from the passphrase
	key, params = kdf(passphrase)
	# encrypt the mnemonic
	ciphertext, tag, nonce = encrypt(key, mnemonic)
	return f'{b64encode(ciphertext).decode()}.{b64encode(tag).decode()}.{b64encode(nonce).decode()}.{b64encode(params.encode()).decode()}'

def decrypt_mnemonic(ciphermnemonic, passphrase):
	''' Decrypt a valid, serialized <ciphertext.tag.nonce> structure '''
	# parse the ciphertext, mac, and nonce from the input ciphermnemonic
	ciphertext, tag, nonce, time, mem, cores = parse_ciphermnemonic(ciphermnemonic)
	# derive the key from the passphrase
	key = kdf_decrypt(passphrase, time, mem, cores)
	return decrypt(key, ciphertext, tag, nonce)

def parse_ciphermnemonic(ciphermnemonic):
	''' Parse the serialized ciphermnemonic <ciphertext.tag.nonce>'''
	try:
		parsed = [b64decode(x) for x in ciphermnemonic.split('.')]
		# split key parameters
		key_params = parsed.pop().decode().split(";")
		parsed += key_params
		if (len(parsed) != 6):
			raise ValueError('Insufficient ciphermnemonic arguments.')
		return parsed
	except Exception as e:
		print(e)

def help():
	''' Print the functions command page '''
	print('Valid arguments: -e, -d, -h')
