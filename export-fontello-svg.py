import argparse
import os
from xml.etree import ElementTree
from base64 import b64encode
import re


parser = argparse.ArgumentParser(
    description='Generate SVG files')
parser.add_argument('--svg-file', dest='svg_file',
                    help='path to svg file to convert')
parser.add_argument('--dest', dest='dest', default='output',
                    help='Path to destination directory')

this_dir = os.path.dirname(os.path.realpath(__file__))


SVG_TEMPLATE = \
"""<svg viewBox=""><path d="{path}"/></svg>"""


def write_file(path, data):
    fi = open(path, 'w')
    fi.write(data)
    fi.close()

if __name__ == '__main__':
    # getting run as a script
    args, _ = parser.parse_known_args()
    if not args.svg_file or not args.dest:
        print(parser.format_usage())
    if not os.path.exists(args.svg_file):
        raise Exception("Invalid svg file path")

    fi = open(args.svg_file)
    svg_data = fi.read()
    fi.close()
    svg_data = re.sub(' xmlns="[^"]+"', '', svg_data)
    tree = ElementTree.fromstring(svg_data)

    if not os.path.exists(args.dest):
        os.makedirs(args.dest)

    for glyph in tree.find('defs').find('font').findall('glyph'):
        svg = SVG_TEMPLATE.format(path=glyph.attrib['d'])
        name = glyph.attrib['glyph-name']
        print('exporting ' + name)
        write_file(os.path.join(args.dest, name + '.svg'), svg)
        write_file(os.path.join(args.dest, name + '.svg.b64'), b64encode(svg))
