import argparse
import sys

class Command(object):
    def __init__(self,prog,description):
        # prog=sys.argv[0], description描述语
        self.parser = argparse.ArgumentParser(prog=prog, description=description)
        self.args = None

    def add_args(self):
        self.parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1', help='show version of program and exit')

    def show(self):
        if len(sys.argv) == 1:
            # 无参显示usage
            self.parser.print_usage()
        else:
            self.parser.parse_args()

    def get_args(self):
        self.args = self.parser.parse_args()

# 参数为Command对象
def command_init(command_object):
    command_object.add_args()
    command_object.show()
    command_object.get_args()

    return command_object

if __name__=='__main__':
    cmd = command_init(Command("cmd","cmd"))
    
