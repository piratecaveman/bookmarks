import copy
import json
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

    def elemental_merge(self, dict_one, dict_two):
        result = copy.deepcopy(dict_one)
        for key, value in dict_two.items():
            if key not in result:
                result[key] = copy.deepcopy(value)
            else:
                if isinstance(result[key], dict):
                    if int(result[key]['lastModified']) > int(value['lastModified']):
                        pass
                    else:
                        result[key] = self.elemental_merge(result[key], value)
                elif isinstance(result[key], list):
                    for item in range(len(result[key])):
                        result[key][item] = self.elemental_merge(result[key][item], value[item])
                else:
                    pass
        return result

    def merge(self):
        result = reduce(self.elemental_merge, self.parsed_files, {})
        return result

    def dump(self, path):
        path = pathlib.Path(path)
        directory = path.parent
        if pathlib.Path.exists(directory):
            with open(path, 'w') as file:
                file.write(json.dumps(self.merge(), indent=4))
        else:
            raise FileNotFoundError(f"Directory {directory} not found!")
