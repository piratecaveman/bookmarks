import re


class TagMeta(object):
    """
    Based Tag Master dissector
    """
    def __init__(self, string):
        self.string = string

    @property
    def stripped_string(self):
        lstripped = self.string.lstrip(' ')
        if lstripped.startswith('<DT'):
            stripped = lstripped[4:]
            return stripped
        else:
            return lstripped

    @property
    def name(self):
        pattern = re.compile(r'<([\w]+)')
        matches = re.findall(pattern, self.stripped_string)
        if matches:
            return matches[0]

    @property
    def text(self):
        pattern = re.compile(r'>(.*?)</')
        matches = re.findall(pattern, self.stripped_string)
        if matches:
            return matches[0]

    @property
    def attributes(self):
        pattern = re.compile(r'([\w]+)=\"(.*?)\"')
        matches = re.findall(pattern, self.stripped_string)
        if matches:
            attribs = {}
            for item in matches:
                attribs[item[0]] = int(item[1]) if item[1].isdigit() else item[1]
            return attribs
