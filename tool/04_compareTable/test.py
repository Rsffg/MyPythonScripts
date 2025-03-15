import sys


if len(sys.argv) > 1:
    received_arg = sys.argv[1]
    print(f'received_arg: {received_arg}')
else:
    print('引数なしです')