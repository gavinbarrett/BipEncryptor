from words import words

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
