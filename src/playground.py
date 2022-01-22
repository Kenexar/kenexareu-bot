import argparse

parser = argparse.ArgumentParser(description='Process')
parser.add_argument('colores', metavar='N', type=int, nargs='-', help='coggers')
print(parser.parse_args(['--']))
