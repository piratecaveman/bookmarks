import re


class TagMeta(object):
    """
    An html tag element
    """
    def __init__(self, string):
        self.string = string

    @property
    def name(self):
        pattern = re.compile(r'<([\w\d]+?)')
        matches = re.findall(pattern, self.string)
        if matches:
            return matches[0]
        else:
            return False

    @property
    def attributes(self):
        pattern = re.compile(r'<(?:[\w\d]+?) (.*?)>')
        matches = re.findall(pattern, self.string)
        if matches:
            tags = {}
            things = matches[0].split('\" ')
            for item in things:
                item = item + '"'
                name, value = re.findall(r'(.*?)="(.*?)"', item)[0]
                if value.isdigit():
                    value = int(value)
                tags[name] = value
            return tags
        else:
            return False

    @property
    def text(self):
        pattern = re.compile(r'<.*\s*?>(.*|\s*)</.*>')
        matches = re.findall(pattern, self.string)
        if matches:
            return matches[0]
        else:
            return False

    @property
    def is_wrapper(self):
        if '<DL>' in self.string:
            return True
        elif '</DL>' in self.string:
            return True
        else:
            return False
