import os
import sys
import re
from zipfile import ZipFile
import urllib.request

def get_requirements_from_whl(file_location):
    f = ZipFile(file_location)
    metadata_file = [file for file in f.filelist if 'METADATA' in str(file)][0]
    metadata = f.read(metadata_file).splitlines()
    metadata = [str(line)[2:-1] for line in metadata]
    reqs = [line.split(': ')[-1] for line in metadata if 'Requires-Dist' in line]
    req_dict = {}
    for row in reqs:
        key = row.split()[0]
        try:
            value = row.split()[1].strip('()')
        except IndexError:
            value = None
        req_dict.update({key: value})
    return req_dict

def get_pip_list():
    pip_list = os.system('pip list')
    div_row = [row for row in pip_list if '---' in row][0]
    div_row_ind = pip_list.index(div_row)
    pip_list = pip_list[div_row_ind+1:]
    pip_list = {row.split()[0]: row.split()[1] for row in pip_list}
    return pip_list


def check_version(ver_installed, ver_needed):
    if not ver_needed:
        return True
    comp_type = re.match(r'^[><=]*', ver_needed)[0]
    ver_needed_list = ''.join(ver_needed[len(comp_type):].split('.'))
    ver_installed_list = ''.join(ver_installed.split('.'))
    return eval(str(float(ver_installed_list)) + comp_type + str(float(ver_needed_list)))
    return True


if __name__ == '__main__':
    # filename = 'PyQt5_sip-12.8.1-cp38-cp38-win_amd64.whl'
    # f = f'../../Downloads/Python Packages/{filename}'
    f = sys.argv[1]

    reqs = get_requirements_from_whl(f)
    # pip_list = get_pip_list()
    print("Package requirements:")
    for req in reqs:
        print(req, reqs[req])
    # print("Uninstalled Packages")
    # for key in reqs:
    #     if key in pip_list:
    #         print(pip_list[key], reqs[key], check_version(pip_list[key], reqs[key]))
    input('Press ENTER to close')
