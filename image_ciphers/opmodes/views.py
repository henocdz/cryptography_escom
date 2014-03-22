from __future__ import division
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, StreamingHttpResponse, Http404
from . import OperationModes as op
from .HillCipher import HillCipher as hc
from .Tools import mod, file_format, get_colors, save_image, create_zip
from zipfile import ZipFile
import tempfile
import json
import os

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
    res = {
        'status': False,
        'current_progress': 0,
        'errors': False,
        'status_txt': 'No has seleccionado una imagen',
        'total_imgs': 0,
    }
    def __process_encrypt():
        
        paths = []
        hill_instance = hc(key=KEY, ikey= KEY_INVERSE)
        ecb = op.ECB(cipher_instance = hill_instance)

        res = {
            'status': False,
            'current_progress': 0,
            'errors': False,
            'status_txt': 'Encrypted with: 0/n ciphers',
            'total_imgs': 0,
            'zip_id': None
        }

        
        _file = request.FILES['original_img']
        ext = file_format(_file)
        colors, size = get_colors(_file)
        e_colors = []

        """ >>> ECB """
        for i,color in enumerate(colors):
            e_colors.append(ecb.encrypt(p=color))            

        for i, color in enumerate(e_colors):
            e_colors[i] = mod(color, 256)

        hill_path = save_image(e_colors, size)        
        paths.append(hill_path)

        res['total_imgs'] = 1
        res['status_txt'] = 'Encrypted with: %d/%d ciphers' % (res['total_imgs'], 5)
        #yield json.dumps(res)

        """ >>> CBC """
        

        """ >>> CREATE ZIPFILE """
        zip_path = create_zip(paths, _file.name.split('.')[0], ext)
        print 'ho'
        res['zip_id'] = zip_path.split('/')[-1].split('.zip')[0]
        print 'li'
        yield json.dumps(res)


    if 'original_img' in request.FILES:
        return StreamingHttpResponse(__process_encrypt())
    else:
        return HttpResponse(json.dumps(res), content_type='application/json')

def modes_operation_decrypt(request):
    """-"""
    pass

def get_zip(request, temp_zip):
    zip_path = "/tmp/%s.zip" % temp_zip
    try:
        zip_file = open(zip_path)
    except:
        raise Http404
    fw = FileWrapper(zip_file)
    os.remove(zip_path)
    response = HttpResponse(fw, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="%s_encrypted.zip"' %  temp_zip

    return response
    