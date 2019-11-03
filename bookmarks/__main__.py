import argparse
import pathlib


from bookmarks.parser.parser import Parser
from bookmarks.merger.merger import Merger


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    cwd = pathlib.Path.cwd()
    print(f"Current working directory is {cwd}")
    bookmarks_path = cwd / 'bookmarks.html'
    json_path = cwd / 'bookmarks.json'
    parser.add_argument(
        '-f',
        '--file',
        action='append',
        dest='files',
        default=bookmarks_path,
        help='file to be parsed'
    )
    parser.add_argument(
        '-o',
        '--output',
        action='store',
        dest='output_file',
        default=json_path,
        help='path to output file'
    )
    args = parser.parse_args()
    if len(args.files) == 1:
        b_parser = Parser()
        b_parser.parse(args.files[0])
        b_parser.dump(args.output_file)
    else:
        merger = Merger(*args.files)
        merger.dump(args.output_file)
    exit()
