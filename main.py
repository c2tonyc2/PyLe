from pyle_sort import sort
from pyle_distribute import distribute
from ast import literal_eval
import argparse

command_list = {
            "distribute":distribute,
            "sort": sort,
}

parser = argparse.ArgumentParser(description='Cabinet options.')
parser.add_argument('command', metavar='cmd', type=str, nargs=1,
                    default="", help="pyle command to execute.")
parser.add_argument('parameter', metavar='param', type=str, nargs=1,
                    default="", help="main parameter to apply to cmd.")
parser.add_argument('directory', metavar='dir', type=str, nargs=1,
                    default="", help="path of the directory to sort.")
parser.add_argument('--o', metavar='options', type=str,
                    dest='options', default="{}",
                    help="dict of optional parameters to a command i.e.\n"
                    "\"{'step':'hour'}\"")

def launcher(args):
    command = command_list[args.command[0]]
    directory = args.directory[0]
    command(directory, args.parameter[0], literal_eval(args.options))
    return

if __name__ == '__main__':
    # python main.py sort time test_files
    args = parser.parse_args()
    launcher(args)
