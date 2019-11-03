import json
import re


from bookmarks.paths.paths import PathCode
from bookmarks.parser.tags import TagMeta


class Parser(object):
    """
    Based Parser
    """
    def __init__(self):
        self.path_code = PathCode()
        self.typecode = {
            1: 'text/x-moz-place',
            2: 'text/x-moz-place-container'
        }
        self.tree = {
            'root': {},
            'menu': {
                'guid': 'menu________',
                'title': 'menu',
                'index': 0,
                'dateAdded': '',
                'lastModified': '',
                'id': 2,
                'typeCode': 2,
                'type': self.typecode[2],
                'root': 'bookmarksMenuFolder',
                'children': []
            }
        }
        self.folder_queue = ['menu']

    def set_file(self, path):
        path = self.path_code.path_tool(path)
        if self.path_code.path_tool.exists(path):
            self.__setattr__('file', path)
            self.__setattr__('content', None)
        else:
            raise FileNotFoundError(f"{path} does not exist!")

    def read_file(self):
        if not hasattr(self, 'file'):
            raise AttributeError("No file set to read!")
        else:
            with open(self.file, 'r') as file:
                content = file.readlines()
                self.__setattr__('content', content)
                self.__setattr__('oldest_stamp', self.oldest('\n'.join(content)))
                self.__setattr__('newest_stamp', self.newest('\n'.join(content)))

    def parse(self, file_path):
        self.set_file(file_path)
        self.read_file()
        folder_index = 0
        url_index = 0
        _id = 2
        for item in self.content:
            if '<DT><H3' in item:
                _id = _id + 1
                tags = TagMeta(item)
                self.folder_queue.append(tags.text)
                meta_content = {
                    'guid': f'{tags.text.strip(" ")}________',
                    'title': tags.text,
                    'index': folder_index,
                    'dateAdded': tags.attributes['ADD_DATE'],
                    'lastModified': tags.attributes['LAST_MODIFIED'],
                    'id': _id,
                    'typeCode': 2,
                    'type': self.typecode[2],
                    'children': []
                }
                folder_index = folder_index + 1
                self.nested_adder(self.folder_queue, meta_content, typecode=2)
            elif '</DL>' in item:
                self.folder_queue.pop(-1)
            elif '<DT><A' in item:
                _id = _id + 1
                tags = TagMeta(item)
                meta_content = {
                    'guid': f'{tags.text.strip(" ")}________',
                    'title': tags.text,
                    'index': url_index,
                    'dateAdded': tags.attributes['ADD_DATE'],
                    'lastModified': tags.attributes['LAST_MODIFIED'],
                    'id': _id,
                    'typeCode': 1,
                    'tags': tags.attributes.get('TAGS', None),
                    'type': self.typecode[1],
                    'uri': tags.attributes['HREF']
                }
                self.nested_adder(self.folder_queue, meta_content, typecode=1)
                url_index = url_index + 1
            else:
                continue
        self.tree['root'] = {
            'guid': 'root________',
            'title': '',
            'index': 0,
            'dateAdded': self.oldest_stamp,
            'lastModified': self.newest_stamp,
            'id': 1,
            'typeCode': 2,
            'type': self.typecode[2],
            'root': 'placesRoot',
            'children': [self.tree['menu']]
        }
        self.tree['menu']['dateAdded'] = self.oldest_stamp
        self.tree['menu']['lastModified'] = self.newest_stamp
        return self.tree['root']

    def nested_adder(self, queue, values, typecode=1):
        if not queue:
            return
        elif len(queue) == 1:
            folder = self.tree[queue[0]]
            folder['children'].append(values)
            return
        else:
            folder = self.tree[queue[0]]
            for item in queue[1:]:
                if item not in folder.keys():
                    folder[item] = values
                    return
                else:
                    folder = folder[item]
            if typecode == 1:
                folder['children'].append(values)
            else:
                return

    @staticmethod
    def oldest(string):
        pattern = re.compile(r'([\d]{10})\"')
        matches = re.findall(pattern, string)
        old = min(int(i) for i in matches)
        return old

    @staticmethod
    def newest(string):
        pattern = re.compile(r'([\d]{10})\"')
        matches = re.findall(pattern, string)
        new = max(int(i) for i in matches)
        return new

    def dump(self, file_path):
        with open(file_path, 'w') as file:
            file.write(json.dumps(self.tree['root'], indent=4))
