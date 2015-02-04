import subprocess

# run your program and collect the string output
cmd = "python slave02.py -a dsfsdfsdf"
out_str = subprocess.check_output(cmd, shell=True)

# See if it works.
# print(out_str)
