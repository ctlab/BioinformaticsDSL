import os
import xml.etree.ElementTree as ET
from collections import defaultdict as ddict

class PackageManager:
    def __init__(self, path=None):
        self._package_dir = path if path is not None else os.path.join(os.getcwd(), 'Utils')
        self._package_map = ddict(list)
        self._pl_list = []
        self._search_packages(self._package_dir)

    def get_pl_list(self):
        return self._pl_list

    def _add_package(self, subdir, filename):
        path = os.path.join(subdir, filename)
        try:
            root = ET.parse(path).getroot()
        except:
            raise RuntimeError('cant read package' + path)

        package = subdir[len(os.path.commonprefix((subdir, self._package_dir))) + 1:]
        self._pl_list.append((package, filename.split('.')[0]))

        if 'implements' in root.attrib:
            self._package_map[root.attrib['implements']].append(path)

    
    def _search_packages(self, path):
        for subdir, dirs, files in os.walk(path):
            for filename in files:
                if filename.split('.')[-1] == 'xml':
                    self._add_package(subdir, filename)

    def get_implementations(self, key):
        return self._package_map[key]

    def find_interface(self, pkg, name):
        interface = os.path.join(self._package_dir, 'interfaces', pkg, name + '.xml')
        if os.path.isfile(interface):
            try:
                root = ET.parse(interface).getroot()
                key = root.attrib['key']
            except:
                raise RuntimeError('cant read interface', interface)

            return key

    def find_pipeline(self, pkg, name):
        pipeline = os.path.join(self._package_dir, pkg, name + '.xml')
        if os.path.isfile(pipeline):
            return pipeline
        return None

    def get_header(self):
        header = open('test.sh')
        return header.read()

