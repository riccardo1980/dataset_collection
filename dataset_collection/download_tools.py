import os
from urllib import request
import zipfile

def get(url):
    with request.urlopen(url) as r:
        return r.read()

def download(url, file=None):
    
    if not file:
        file = url.split('/')[-1]

    with open(file, 'wb') as f:
        f.write(get(url))

def download_extract(url, target):
    
    os.makedirs(target)
    zip_file = os.path.join(target, url.split('/')[-1])

    # download and unzip
    download(url, zip_file)
            
    with zipfile.ZipFile(zip_file,'r') as zip_ref:
        zip_ref.extractall(target)

    os.remove(zip_file)