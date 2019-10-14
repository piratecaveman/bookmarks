import json


from bookmarks.tags import TagMeta
from bookmarks.paths import PathCode


class Parser(object):
    """
    Based Parser
    """
    def __init__(self):
        self.tree = {
            'root': {},
        }
        self.paths = PathCode()

    def read(self, path=None):
        path = self.paths.make_path(path) if path is not None \
            else self.paths.pathlibPath(self.paths.pathlibPath.cwd() / 'bookmarks.html')
        with open(str(path), 'r') as file:
            content = file.readlines()
        return content

    @staticmethod
    def strip_header(split_document):
        if 'DOCTYPE' in split_document[0]:
            return split_document[6:]
        else:
            return split_document

    def parse(self, document):
        if isinstance(document, str):
            cache = self.strip_header(document.split('\n'))
        else:
            cache = self.strip_header(document)
        folder_que = ['root']
        for item in cache:
            if '<DT><H3' in item:
                tag = TagMeta(item)
                folder_que.append(tag.text)
                self.nested_adder(folder_que, tag.attributes)
            elif '</DL>' in item:
                folder_que.pop(-1)
            elif '<A' in item:
                copy = item.lstrip(' ')[4:]
                tag = TagMeta(copy)
                data = {
                    'title': tag.text,
                    'dateAdded': tag.attributes['ADD_DATE'],
                    'lastModified': tag.attributes['LAST_MODIFIED'],
                    'uri': tag.attributes['HREF'],
                }
                if 'TAGS' in tag.attributes.keys():
                    data['tags'] = tag.attributes['TAGS']
                self.nested_adder(folder_que, data)
            else:
                pass
        return self.tree

    def nested_adder(self, que, value):
        if not que:
            return
        nest = self.tree.copy()
        re_que = que.copy()
        folder = nest[re_que[0]]
        for item in re_que[1:]:
            if item not in folder.keys():
                folder[item] = {}
            folder = folder.get(item, {})
            if item == re_que[-1]:
                folder['children'] = folder.get('children', [])
                folder['children'].append(value)
        self.tree.update(nest)

    def dump(self, path=None):
        path = self.paths.make_path(path) if path is not None else str(self.paths.pathlibPath.cwd() / 'bookmarks.json')
        with open(path, 'w') as f:
            f.write(json.dumps(self.tree, indent=4))
