import argparse

# Initialize argument parse object
parser = argparse.ArgumentParser(description='This is the description')

# This would be an argument you could pass in from command line
# parser.add_argument('-o', action='store', dest='o', type=str, required=True,
#                     default='hello world')
parser.add_argument('-a', action="store_true", default=False)
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)

# print(parser.parse_args(['-a', '-bval', '-c', '3']))
results = parser.parse_args()
print(results)

# Parse the arguments
# inargs = parser.parse_args()
# arg_str = inargs.o

# # print the command line string you passed (default is "hello world")
# print(str(arg_str))
