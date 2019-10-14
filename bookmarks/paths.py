import pathlib


class PathCode(object):
    """
    Contains paths for internal use
    """
    def __init__(self):
        self.pathlibPath = pathlib.Path
        self.base = pathlib.Path(__file__).parent
        self.blob = pathlib.Path(self.base) / 'blobs'

    @staticmethod
    def make_path(string):
        if '\\' in string:
            path = pathlib.PureWindowsPath(string)
        else:
            path = pathlib.PurePosixPath(string)
        return path
