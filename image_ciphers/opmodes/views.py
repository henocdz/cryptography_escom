from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from . import OperationModes as op
from .HillCipher import HillCipher as hc
from .Tools import mod, file_format, get_colors, save_image
import json

KEY = [[1,2,3],[4,5,6],[11,9,8]]
KEY_INVERSE = [[90,167,1],[74,179,254],[177,81,1]]

def home(request):
    """Project home"""
    return render_to_response('index.html', locals())

def index(request):
    """-"""
    pass

def modes_operation(request):
    return render_to_response('modes_op.html', locals(), RequestContext(request))

def modes_operation_encrypt(request):
    hill_instance = hc(key=KEY, ikey= KEY_INVERSE)
    ecb = op.ECB(cipher_instance = hill_instance)

    res = {
        'code': 200,
        'errors': False,
        'error_txt': 'No has seleccionado una imagen'
    }
    
    if 'original_img' in request.FILES:
        _file = request.FILES['original_img']
        ext = file_format(_file)
        colors, size = get_colors(_file)

        e_colors = []
        i=0
        for color in colors:
            e_colors.append(ecb.encrypt(p=color))

        for i, color in enumerate(e_colors):
            e_colors[i] = mod(color, 256)

        print save_image(e_colors, size)

        res = {
            'code': 200,
            'errors': False,
            'status_txt': 'Sin errores compi :)',
            'zip_id': 13452342456
        }

    return HttpResponse(json.dumps(res), content_type='application/json')

def modes_operation_decrypt(request):
    """-"""
    pass

def download_temp(request, temp):
    pass