import argparse
import os


from bookmarks.parser import Parser
from bookmarks.merge import Merger


if __name__ == '__main__':
    cwd = os.getcwd()
    print(f"Current Directory: {cwd}")
    bookmarks_path = os.path.join(cwd, 'bookmarks.html')
    json_path = os.path.join(cwd, 'bookmarks.json')
    parser = Parser()
    argp = argparse.ArgumentParser()
    argp.add_argument(
        '-f',
        '--file',
        action='append',
        dest='file',
        default=[bookmarks_path],
        help="""        Name or path to the Netscape html bookmarks file / files"""
    )
    argp.add_argument(
        '-o',
        '--output',
        action='store',
        dest='output',
        default=json_path,
        help="""        Name or path to store output file"""
    )
    args = argp.parse_args()
    if len(args.file) == 1:
        document = parser.read(args.file)
        parser.parse(document)
        parser.dump(args.output)
    else:
        merger = Merger(*args.file)
        merger.dump(args.output)
    exit()
