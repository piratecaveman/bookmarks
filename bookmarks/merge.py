import pathlib
import re
import json
import functools
from collections.abc import Mapping


import bookmarks.parser


class Merger(object):
    """
    Merge elements
    """
    def __init__(self, *args):
        self.files = args

    @staticmethod
    def read_file(file):
        with open(file, 'r') as f:
            document = f.readlines()
        return document

    @property
    def data(self):
        aggregate = []
        for file in self.files:
            if pathlib.Path(file).exists():
                document = self.read_file(file)
                aggregate.append(document)
            else:
                continue
        return aggregate

    @staticmethod
    def parse_document(document):
        parser = bookmarks.parser.Parser()
        parsed = parser.parse(document)
        return parsed

    @property
    def dictionaries(self):
        aggregate = []
        for doc in self.data:
            parsed_doc = self.parse_document(doc)
            aggregate.append(parsed_doc)
        return aggregate

    @staticmethod
    def merge_element(dictionary_one, dictionary_two):
        if not dictionary_one:
            return dictionary_two
        pattern = re.compile(r'([\d]{10,})')
        match_one = re.findall(pattern, json.dumps(dictionary_one))
        match_two = re.findall(pattern, json.dumps(dictionary_two))
        max_one = max(*match_one)
        max_two = max(*match_two)

        def actual(main, supplementary):
            for key, value in supplementary.items():
                if key in main and isinstance(main[key], dict) and isinstance(supplementary[key], Mapping):
                    actual(main[key], supplementary[key])
                else:
                    main[key] = supplementary[key]

        if max_one > max_two:
            actual(dictionary_two, dictionary_one)
            return dictionary_two
        else:
            actual(dictionary_one, dictionary_two)
            return dictionary_one

    def merge_all(self):
        result = functools.reduce(self.merge_element, self.dictionaries, {})
        return result

    def dump(self, f_path=None):
        path = pathlib.Path(f_path) if f_path is not None else str(pathlib.Path.cwd() / 'bookmarks.json')
        with open(path, 'w') as f:
            f.write(json.dumps(self.merge_all(), indent=4))
