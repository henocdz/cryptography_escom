from .Tools import clean_data, list_xor, mod

class ECB:
	"""Electronic code book"""
	def __init__(self, cipher_instance, *args, **kwargs):
		self.cipher = cipher_instance

	def encrypt(self, p):
		return_string = False
		if type(p) is str or type(p) is unicode:
			return_string = True
		
		p = clean_data(data=p)
		encrypted = self.cipher.encrypt(plain_text=p)

		if return_string:
			return ''.join(encrypted)
		return encrypted

	def decrypt(self, c):
		return self.cipher.decrypt(cipher_text=c)

class CBC:
	"""Cipher block chaining"""
	def __init__(self, cipher_instance, init_vector, *args, **kwargs):
		self.prev = init_vector
		self.cipher = cipher_instance
		
	def encrypt(self, p):
		p = clean_data(data=p)
		xored = list_xor(self.prev, p)
		encrypted = self.cipher.encrypt(plain_text=xored)
		self.prev = list(mod(encrypted, 256))

		return encrypted

	def decrypt(self, d):
		pass


class CFB:
	"""Cipher feedback"""
	pass

class OFB:
	"""Output feedback"""
	pass

class CTR:
	"""Counter Mode"""
	pass

