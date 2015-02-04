import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'square',
    help='Returns the square of the parameter',
    type=int)
parser.add_argument(
    '-v', '--verbose', help='increase output verbosity',
    action='store_true')

# parser.add_argument('echo', help='Repeat parameter')
args = parser.parse_args()
if args.verbose:
    print('verbosity turned on')
print(args.square**2)
