import abc
import os
from typing import List, Tuple, Dict


class datasetABC(abc.ABC):
    """
        Class for accessing <DATASET_NAME> dataset

        Dataset is described here: <URL>
    """

    def __init__(self,
                 data_root: str = os.path.join(os.path.expanduser('~'),
                                               'dataset_collection_data')) -> None:
        """
            Download resource

            :param str data_root: Folder used as base for data download and store
            :rtype: None
        """
        # self._base_folder = os.path.join(data_root, 'tiny-imagenet-200')
        # self._resource_uri = 'http://cs231n.stanford.edu/tiny-imagenet-200.zip'
        pass

    @abc.abstractmethod
    def get_description_map(self) -> Dict[str, str]:
        """
            Returns a dict with labels as key and description as value

            :rtype: Dict[str,str]
        """
        pass

    @abc.abstractmethod
    def get_train_dataset(self) -> Tuple[List[str], List[str]]:
        """
            Returns a uris and labels

            :rtype: Tuple[List[str], List[str]]
        """
        pass

    @abc.abstractmethod
    def get_val_dataset(self) -> Tuple[List[str], List[str]]:
        """
            Returns a uris and labels

            :rtype: Tuple[List[str], List[str]]
        """
        pass
