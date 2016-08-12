import os
import datetime
import shutil

TIME_STEP = "day"
NAME_POS = "contains"

#TODO currently moves both files and directories, may want to reconsider this
#TODO add assertion for files
def sort(source, parameter, options):
    destination = source
    if "dest" in options:
        destination = options["dest"]
    parameter_list[parameter](source, destination, options)
    return

def time_sort(source, destination, options):
    if "step" in options:
        TIME_STEP = options["step"]
    for filename in os.listdir(source):
        path = os.path.join(source, filename)
        try:
            subfolder = getattr(get_mod_datetime(path), TIME_STEP)
            create_and_move(path, os.path.join(destination, str(subfolder)))
        except AttributeError:
            print(TIME_STEP + " is not a valid parameter.")

def get_mod_datetime(filename):
    return datetime.datetime.fromtimestamp(
           os.path.getmtime(filename))

def name_sort(source, destination, options):
    if "pos" in options:
        NAME_POS = options["pos"]
    subfolder = options["name"]
    for filename in os.listdir(source):
        path = os.path.join(source, filename)
        name = os.path.splitext(path)[0]
        if NAME_POS == "start" and name.startswith(subfolder) or \
        NAME_POS == "end" and name.endswith(subfolder) or \
        NAME_POS == "contains" and subfolder in name:
            create_and_move(path, os.path.join(destination, str(subfolder)))
    return

def ext_sort(source, destination, options):
    """Files without an extension or end in a period are not sorted.
    """
    for filename in os.listdir(source):
        path = os.path.join(source, filename)
        subfolder = os.path.splitext(path)[1]
        if len(subfolder) >= 2:
            create_and_move(path, os.path.join(destination, str(subfolder)))
    return

def create_and_move(current_path, new_path):
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    shutil.move(current_path, new_path)

parameter_list = {
    'time': time_sort,
    'name': name_sort,
    'ext': ext_sort
}
