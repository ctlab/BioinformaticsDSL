#!/usr/bin/python3
import os
import sys


class Shell:
    def __init__(self, work_dir):
        self._work_dir = work_dir

    def get_stamps(self):
        for subdir, dirs, files in os.walk(self._work_dir):
            for file in files:
                print(os.path.join(subdir, file))


    def run(self):
        self.get_stamps()
        print('>>> ', end="", flush=True)
        for line in sys.stdin:
            output = os.popen(line).read()
            print(output)
            print('>>> ', end="", flush=True)


def main():
    shell = Shell('workdir/mntpoint')
    shell.run()

if __name__ == '__main__':
    main()