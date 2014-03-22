class ECB:
	"""Electronic code book"""
	def __init__(self, cipher_instance, *args, **kwargs):
		self.cipher = cipher_instance

	def __clean(self, data):
		p = list(data)		
		for i, e in enumerate(p):
			if type(e) is str or type(e) is unicode:
				p[i] = ord(e)
		return p

	def encrypt(self, p):
		return_string = False
		if type(p) is str or type(p) is unicode:
			return_string = True
		
		p = self.__clean(data=p)
		encrypted = self.cipher.encrypt(plain_text=p)

		if return_string:
			return ''.join(encrypted)
		return encrypted

	def decrypt(self, c):
		return self.cipher.decrypt(cipher_text=c)

class CBC:
	"""Cipher block chaining"""
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

