import argparse

# Initialize argument parse object
parser = argparse.ArgumentParser()

# This would be an argument you could pass in from command line
parser.add_argument('-o', action='store', dest='o', type=str, required=True,
                    default='hello world')

# Parse the arguments
inargs = parser.parse_args()
arg_str = inargs.o

# print the command line string you passed (default is "hello world")
print(arg_str)
