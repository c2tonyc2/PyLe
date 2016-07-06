import os
import datetime
import shutil

TIME_STEP = "day"
NAME_POS = "contains"

#TODO add assertion for files
def sort(directory, parameter, options):
    parameter_list[parameter](directory, options)
    return

def time_sort(directory, options):
    if "step" in options:
        TIME_STEP = options["step"]
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        try:
            subfolder = getattr(get_mod_datetime(path), TIME_STEP)
            create_and_move(directory, filename, path, subfolder)
        except AttributeError:
            print(TIME_STEP + " is not a valid parameter.")

def get_mod_datetime(filename):
    return datetime.datetime.fromtimestamp(
           os.path.getmtime(filename))

def name_sort(directory, options):
    if "pos" in options:
        NAME_POS = options["pos"]
    subfolder = options["name"]
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        name = os.path.splitext(path)[0]
        if NAME_POS == "start" and name.startswith(subfolder) or \
        NAME_POS == "end" and name.endswith(subfolder) or \
        NAME_POS == "contains" and subfolder in name:
            create_and_move(directory, filename, path, subfolder)
        else:
            create_and_move(directory, filename, path, "Other")
    return

def ext_sort(directory, options):
    """Files without an extension or end in a period are not sorted.
    """
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        subfolder = os.path.splitext(path)[1]
        if len(subfolder) < 2:
            subfolder = ""
        create_and_move(directory, filename, path, subfolder)
    return

def create_and_move(directory, filename, path, subfolder):
    if subfolder:
        newPath = os.path.join(directory, str(subfolder))
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        newPath = os.path.join(newPath, filename)
        shutil.move(path, newPath)

parameter_list = {
    'time': time_sort,
    'name': name_sort,
    'ext': ext_sort
}
