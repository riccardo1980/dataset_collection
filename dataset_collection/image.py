import os
import pathlib
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, BinaryIO

from dataset_collection.download_tools import download_extract
from dataset_collection.base import datasetABC


class tiny_imagenet(datasetABC):
    """
        Class for accessing tiny-imagenet dataset

        Dataset is described here: https://tiny-imagenet.herokuapp.com/
    """

    def __init__(self,
                 data_root: str = os.path.join(os.path.expanduser('~'),
                                               'dataset_collection_data')) -> None:
        """
            Check availability
        """
        self._base_folder = os.path.join(data_root, 'tiny-imagenet-200')
        self._resource_uri = 'http://cs231n.stanford.edu/tiny-imagenet-200.zip'

        # full imagenet classes description
        self._labels_description_file = os.path.join(
            self._base_folder, 'tiny-imagenet-200', 'words.txt')

        # subset of classes in this dataset
        self._labels_list_file = os.path.join(
            self._base_folder, 'tiny-imagenet-200', 'wnids.txt')

        # template for train subfolders in _base_folder
        self._template_train_folders = os.path.join(
            self._base_folder, 'tiny-imagenet-200', 'train', '*', 'images', '*')

        # template for val subfolders in _base_folder
        self._template_val_folders = os.path.join(
            self._base_folder, 'tiny-imagenet-200', 'val', 'images', '*')

        # val set annotations
        self._val_annotations_file = os.path.join(
            self._base_folder, 'tiny-imagenet-200', 'val', 'val_annotations.txt')

        if not os.path.isdir(self._base_folder):
            print('Downloading from: {}'.format(self._resource_uri))
            download_extract(self._resource_uri, self._base_folder)

    def get_description_map(self) -> Dict[str, str]:

        # read full description
        with open(self._labels_description_file) as f:
            df_desc = pd.read_csv(f,
                                  header=None,
                                  names=['label', 'description'],
                                  sep='\t')

        # read labels subset
        with open(self._labels_list_file) as f:
            df_labels = pd.read_csv(f, header=None, names=['label'])

        # join
        df = pd.merge(df_labels, df_desc, how='left',
                      left_on='label', right_on='label')

        label_desc = {item[1]['label']: item[1]['description'] for item
                      in df.iterrows()}
        return label_desc

    def get_train_dataset(self) -> Tuple[List[str], List[str]]:
        """
            Returns a list of URI, label tuples
        """
        root_path = pathlib.Path(self._base_folder)
        images = root_path.glob(self._template_train_folders)
        uris = [img.as_posix() for img in images]
        labels = [uri.split('/')[-3] for uri in uris]
        return uris, labels

    def get_val_dataset(self) -> Tuple[List[str], List[str]]:
        """
            Returns a list of URI, label tuples
        """
        root_path = pathlib.Path(self._base_folder)
        images = root_path.glob(self._template_val_folders)
        uris = [img.as_posix() for img in images]
        df_uris = pd.DataFrame({'uri': uris})
        df_uris['filename'] = df_uris['uri'].map(lambda x: x.split('/')[-1])

        with open(self._val_annotations_file) as f:
            df_uris_labels = pd.read_csv(f,
                                         header=None,
                                         names=['filename', 'label',
                                                'a', 'b', 'c', 'd'],
                                         sep='\t')
            df_uris_labels.drop(columns=['a', 'b', 'c', 'd'], inplace=True)

        df = pd.merge(df_uris, df_uris_labels, how='left',
                      left_on='filename', right_on='filename')[['uri', 'label']]

        uris = df['uri'].tolist()
        labels = df['label'].tolist()

        return uris, labels


class MNIST(datasetABC):
    def __init__(self,
                 data_root: str = os.path.join(os.path.expanduser('~'),
                                               'dataset_collection_data')) -> None:
        """
            Check availability
        """
        self._base_folder = os.path.join(data_root, 'MNIST')
        self._resource_uris = {
            'train-images': 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
            'train-labels': 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
            'test-images': 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
            'test-labels': 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
        }

        self._train_images = os.path.join(self._base_folder,
                                          'train-images-idx3-ubyte')
        self._train_labels = os.path.join(self._base_folder,
                                          'train-labels-idx1-ubyte')
        self._val_images = os.path.join(self._base_folder,
                                        't10k-images-idx3-ubyte')
        self._val_labels = os.path.join(self._base_folder,
                                        't10k-labels-idx1-ubyte')

        if not os.path.isdir(self._base_folder):
            for item, uri in self._resource_uris.items():
                print('Downloading {} from: {}'.format(item, uri))
                download_extract(uri, self._base_folder)

    # low level [TODO] change typing
    def get_train_dataset(self) -> Tuple[List[str], List[str]]:
        with open(self._train_images, 'rb') as f:
            images = _decode_images(f)
        with open(self._train_labels, 'rb') as f:
            labels = _decode_labels(f)

        return images, labels


    # low level [TODO] change typing
    def get_val_dataset(self) -> Tuple[List[str], List[str]]:
        with open(self._val_images, 'rb') as f:
            images = _decode_images(f)
        with open(self._val_labels, 'rb') as f:
            labels = _decode_labels(f)

        return images, labels

    def get_description_map(self) -> Dict[str, str]:
        dmap = {
            '0': 'zero',
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
            '6': 'six',
            '7': 'seven',
            '8': 'eight',
            '9': 'nine',
            }
        return dmap

# low level [TODO] change typing
def _decode_labels(stream: BinaryIO) -> List[str]:
    magic_nr, n_labels = np.fromfile(stream, dtype='>i4', count=2)
    labels = np.fromfile(stream, dtype=np.uint8)

    return labels

# low level [TODO] change typing
def _decode_images(stream: BinaryIO) -> List[str]:
    magic_nr, n_images, rows, cols = np.fromfile(stream, dtype='>i4', count=4)
    images = np.fromfile(stream, dtype=np.uint8)

    return images.reshape(n_images, rows, cols)
