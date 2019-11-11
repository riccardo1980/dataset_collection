import os
import pathlib
import pandas as pd
from dataset_collection.download_tools import download_extract
from typing import List, Tupe

class tiny_imagenet:
    """
        Class for accessing tiny-imagenet dataset

        Dataset is described here: https://tiny-imagenet.herokuapp.com/
    """

    def __init__(self,
                 data_root: str = os.path.join(os.path.expanduser('~'),
                                               'dataset_collection')) -> None:
        """
            Check availability
        """
        self._base_folder = os.path.join(data_root, 'tiny-imagenet-200')
        self._resource_uri = 'http://cs231n.stanford.edu/tiny-imagenet-200.zip'
        # full imagenet classes description
        self._labels_description_file = os.path.join(
            self._base_folder, 'tiny-imagenet-200', 'words.txt')

        # subset of classes in this dataset
        self.__labels_description_file = os.path.join(
            self._base_folder, 'tiny-imagenet-200', 'wnids.txt')

        # template for subfolders in _base_folder
        self._template_train_folders = os.path.join(
            'tiny-imagenet-200', 'train', '*', 'images', '*')

        print('BASE_FOLDER: {}'.format(self._base_folder))

        if not os.path.isdir(self._base_folder):
            download_extract(self._resource_uri, self._base_folder)

    def get_description_map(self) -> Dict[str, str]:

        # read full description
        with open(self._labels_description_file) as f:
            df_desc = pd.read_csv(f,
                                  header=None,
                                  names=['label', 'description'],
                                  sep='\t')

        # read labels subset
        with open(self.__labels_description_file) as f:
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
