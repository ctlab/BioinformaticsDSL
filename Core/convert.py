#!/usr/bin/python3
from os import system
from os import path
import sys
from pipeline import Pipeline
from package_manager import PackageManager
from variant import Variant

def main():
    if len(sys.argv) < 3:
        print('usage:\nconvert <pipeline>.xml <output>.sh (arg_name=arg_value)*')
        return

    pl_file = sys.argv[1]
    script = sys.argv[2]
    args = {arg : Variant.from_string(value, 'string') for (arg, value) in [item.split('=') for item in sys.argv[3:]]}

    pm = PackageManager()
    include_sh = open('Test/diff_expr/include.sh', 'w')
    include_sh.write(pm.get_header())
    include_sh.close()

    pipeline = Pipeline(pl_file, pm)
    out_file = open(script, 'w')
    output = pipeline.generate(args)
    out_file.write('DIR="${BASH_SOURCE%/*}"\n. "$DIR/include.sh"\n\n')
    out_file.write(output)
    out_file.close()
    system('chmod +x ' + script)
    print(output)

if __name__ == '__main__':
    main()