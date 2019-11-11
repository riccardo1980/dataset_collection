import os
from urllib import request
import zipfile

def get(url: str) -> str:
    """
        Get resource to string

        :param str url: location of the resource
        :rtype str

    """

    with request.urlopen(url) as r:
        return r.read()

def download(url: str, file: str = None) -> None:
    """
        Download remote file to local

        :param str url: location of the resource
        :param str file: local file
        :rtype None

    """

    if not file:
        file = url.split('/')[-1]

    with open(file, 'wb') as f:
        f.write(get(url))

def download_extract(url: str, target: str) -> None:
    """
        Download and extraction of remote file

        :param str url: location of the resource
        :param str target: local folder
        :rtype None

    """

    os.makedirs(target)
    temp_file = os.path.join(target, url.split('/')[-1])

    download(url, temp_file)

    if temp_file.endswith('.zip'):
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall(target)
        os.remove(temp_file)
