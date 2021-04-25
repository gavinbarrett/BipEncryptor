from math import floor
from os import cpu_count
from psutil import virtual_memory
from argon2 import hash_password_raw, low_level

white = '\u001b[37m'
end = '\033[0m'

def kdf(passphrase):
	''' Derive the key from a passphrase '''
	print(f'{white}Stretching key...{end}')
	# compute 50 of the available memory
	mem = floor((virtual_memory().free * 0.66)/1000)
	return hash_password_raw(time_cost=8, memory_cost=mem, parallelism=cpu_count(), hash_len=32, password=passphrase, salt=b"k3y der1vati0n", type=low_level.Type.ID)
