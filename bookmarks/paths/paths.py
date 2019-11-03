import pathlib


class PathCode(object):
    """
    Based Path Code
    """
    def __init__(self):
        self.path_tool = pathlib.Path
        self._project_root = pathlib.Path(__file__).parent.parent
        self.blobs_path = self._project_root / 'blobs'
        self.parser_path = self._project_root / 'parser'
        self.root = self._project_root
