import os

class Singleton:
    """Alex Martelli implementation of Singleton (Borg)
    http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html"""

    """https://stackoverflow.com/questions/44237186/what-is-the-best-way-to-share-data-between-widgets-with-pyqt"""
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Database(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        
    def get(self):
        return self._data

    def set(self, **data):
        # For example from csv or binary files using
        # np.genfromtxt or np.fromfile
        self._data = data


class Cache:  # eg global config object, I discourage actually using this pattern
    """https://www.youtube.com/watch?v=-zsV0_QrfTw"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            Cache().__init_data__()
        return cls._instance

    def __init_data__(self) -> None:
        self.data = {}

    def get(self, attr:str):
        return self.data.get(attr, '')
    
    def set(self, **data):
        if 'modelDir' in data.keys():
            data['modelDir'] = os.path.join(os.path.dirname(__file__), data['modelDir'])
        self.data.update(data)
        
        