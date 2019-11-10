import os
import pathlib
import pandas as pd

class tiny_imagenet:
    """
        returns a dictionary of label description maps
    """
    
    def __init__(self, DATASET_ROOT):
        self._DATASET_ROOT = DATASET_ROOT
        self._FULL_DESC_FILE = os.path.join(self._DATASET_ROOT, 'words.txt') # classes description
        self._LABELS_FILE = os.path.join(self._DATASET_ROOT, 'wnids.txt') # subset of classes in this dataset
        self._TRAIN_SET_FOLDERS = 'train/*/images/*'

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
        root_path = pathlib.Path(self._DATASET_ROOT)
        images = root_path.glob(self._TRAIN_SET_FOLDERS)
        uris = [ img.as_posix() for img in images ] 
        labels = [ uri.split('/')[-3] for uri in uris ] 
        return uris, labels