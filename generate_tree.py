import os


def return_Tree():
    original_path = os.getcwd()
    path = ''
    path += original_path + '/root/'
    os.chdir(path)
    temp = os.popen("tree -H root").read()
    os.chdir(original_path)
    return temp
