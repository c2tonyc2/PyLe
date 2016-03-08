import os
import datetime
import shutil

TIME_STEP = "day"

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
    return

def ext_sort(directory, options):
    """Files without an extension or end in a period are stored in the
    subfolder OTHER.
    """
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        subfolder = os.path.splitext(path)[1]
        if len(subfolder) < 2:
            subfolder = "Other"
        create_and_move(directory, filename, path, subfolder)
    return

def name_sort(directory, options):
    return

def create_and_move(directory, filename, path, subfolder):
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
