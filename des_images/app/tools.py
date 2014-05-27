from zipfile import ZipFile
import tempfile
import os


def create_zip(paths, filename='demo', ext='bpm'):
    zip_obj, zip_path = tempfile.mkstemp(suffix='.zip')
    _zip = ZipFile(zip_path, 'w')

    ciphers = ['ECB', 'CBC', 'CFB', 'OFB', 'CTR']

    for i, path in enumerate(paths):
        _zip.write(path, "%s_%s.%s" % (filename, ciphers[i], ext))
        os.remove(path)

    _zip.close()

    return zip_path


def chunker(string):
    chunks = [string[s:s+8] for s in range(0, len(string), 8)]
    return chunks
