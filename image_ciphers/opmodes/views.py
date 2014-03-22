from django.shortcuts import render, render_to_response, redirect
from . import OperationModes as op
from .HillCipher import HillCipher as hc
from .Tools import mod

KEY = [[1,2,3],[4,5,6],[11,9,8]]
KEY_INVERSE = [[90,167,1],[74,179,254],[177,81,1]]
colors = [
	[14, 229, 227],
	[5, 217, 212],
	[245, 201, 195],
	[13, 220, 211],
	[13, 220, 211],
	[31, 233, 221],
	[47, 249, 238],
	[47, 249, 238],
	[177, 114, 104],
	[145, 82, 70],
	[113, 50, 36],
	[97, 34, 19],
	[113, 50, 36],
	[129, 66, 53],
	[145, 82, 70],
]
def home(request):
	"""Project home"""
	return render_to_response('index.html', locals())

def index(request):
	"""-"""
	pass

def modes_operation(request):
	return render_to_response('modes_op.html', locals())

def modes_operation_encrypt(request):
	hill_instance = hc(key=KEY, ikey= KEY_INVERSE)
	ecb = op.ECB(cipher_instance = hill_instance)

	e_colors = []
	for color in colors:
		e_colors.append(ecb.encrypt(p=color))
	
	for c in e_colors:
		print mod(c, 256)

def modes_operation_decrypt(request):
	"""-"""
	pass