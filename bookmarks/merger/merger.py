import re
import json
from collections.abc import Mapping
from functools import reduce
import pathlib
from bookmarks.parser.parser import Parser


class Merger(object):
    """
    Based merging deviant
    """
    def __init__(self, *file_paths):
        self._read_files = file_paths

    @property
    def parsed_files(self):
        aggregate = list()
        for file in self._read_files:
            parser = Parser()
            result = parser.parse(file)
            aggregate.append(result)
        return aggregate

    @staticmethod
    def elemental_merge(dict_one, dict_two):
        stamp_one = max(int(stamp) for stamp in re.findall(r'[\d]{10}', json.dumps(dict_one)))
        stamp_two = max(int(stamp) for stamp in re.findall(r'[\d]{10}', json.dumps(dict_two)))

        def nested_merger(main, supplementary):
            for key, value in supplementary.items():
                if key in main and isinstance(main[key], dict) and isinstance(supplementary[key], Mapping):
                    nested_merger(main[key], supplementary[key])
                else:
                    main[key] = supplementary[key]

        if stamp_two >= stamp_one:
            nested_merger(dict_one, dict_two)
            return dict_one
        else:
            nested_merger(dict_two, dict_one)
            return dict_two

    def merge(self):
        result = reduce(self.elemental_merge, self.parsed_files)
        return result

    def dump(self, path):
        path = pathlib.Path(path)
        directory = path.parent
        if pathlib.Path.exists(directory):
            with open(path, 'w') as file:
                file.write(json.dumps(self.merge(), indent=4))
        else:
            raise FileNotFoundError(f"Directory {directory} not found!")
