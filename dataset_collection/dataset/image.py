import os
import pathlib
import pandas as pd
from dataset_collection.download_tools import download_extract

class tiny_imagenet:
    """
        Class for accessing tiny-imagenet dataset

        Dataset is described here: https://tiny-imagenet.herokuapp.com/
    """
    
    def __init__(self, data_root=os.path.join(os.path.expanduser('~'),'dataset_collection')):
        """
            Check availability
        """
        self._BASE_FOLDER = os.path.join(data_root, 'tiny-imagenet-200')
        self._URI = 'http://cs231n.stanford.edu/tiny-imagenet-200.zip'
        # full imagenet classes description 
        self._FULL_DESC_FILE = os.path.join(self._BASE_FOLDER, 'tiny-imagenet-200','words.txt') 
        
         # subset of classes in this dataset
        self._LABELS_FILE = os.path.join(self._BASE_FOLDER, 'tiny-imagenet-200', 'wnids.txt')
        
        # template for subfolders in _BASE_FOLDER
        self._TRAIN_SET_FOLDERS = os.path.join('tiny-imagenet-200','train','*','images','*') 
        
        print('BASE_FOLDER: {}'.format(self._BASE_FOLDER))

        if not os.path.isdir(self._BASE_FOLDER):
            download_extract(self._URI, self._BASE_FOLDER)

    def get_description_map(self):
    
        # read full description
        with open(self._FULL_DESC_FILE) as f:
            df_desc = pd.read_csv(f, header=None, names=['label','description'],sep='\t')

        # read labels subset
        with open(self._LABELS_FILE) as f:
            df_labels = pd.read_csv(f, header=None, names=['label'])

        # join
        df = pd.merge(df_labels, df_desc, how='left', left_on='label', right_on='label')
        
        return { item[1]['label']: item[1]['description'] for item in df.iterrows() }

    def get_train_dataset(self):
        """
            Returns a list of URI, label tuples
        """
        root_path = pathlib.Path(self._BASE_FOLDER)
        images = root_path.glob(self._TRAIN_SET_FOLDERS)
        uris = [ img.as_posix() for img in images ] 
        labels = [ uri.split('/')[-3] for uri in uris ] 
        return uris, labels