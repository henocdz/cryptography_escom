def mod(data, z):
	rdata = []
	for d in data:
		aux = d
		if type(d) is str or type(d) is unicode:
 			aux = ord(d)

		while aux > z:
			aux = aux%z
		rdata.append(aux)
	return rdata