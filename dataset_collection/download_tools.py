import os
import sys
import urllib
import zipfile
import gzip


def download(url: str, filename: str = None) -> None:
    """
        Download remote file to local

        :param str url: location of the resource
        :param str filename: local file
        :rtype None

    """

    def reporthook(count, block_size, total_size):
        progress = min(int(100 * count * block_size / total_size), 100)
        sys.stdout.write('\r... {} % of {} MB'.format(progress,
                                                      total_size//(1024*1024)))

    urllib.request.urlretrieve(url, filename, reporthook)


def download_extract(url: str, target: str) -> None:
    """
        Download and extraction of remote file

        :param str url: location of the resource
        :param str target: local folder
        :rtype None

    """

    if not os.path.isdir(target):
        os.makedirs(target)
    temp_file = os.path.join(target, url.split('/')[-1])

    download(url, temp_file)

    target_filename, comp_extension = os.path.splitext(temp_file)
    if comp_extension == '.zip':
        print(' ... Extracting')
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall(target)
        os.remove(temp_file)

    if comp_extension == '.gz':
        print(' ... Extracting')
        with gzip.open(temp_file, 'rb') as infile:
            with open(target_filename, 'wb') as outfile:
                outfile.write(infile.read())
        os.remove(temp_file)
