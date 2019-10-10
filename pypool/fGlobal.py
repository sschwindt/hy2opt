try:
    import os, logging, sys, glob, webbrowser, time
    from collections import Iterable  # used in the flatten function
    from bisect import bisect_left
except:
    print("ImportERROR: Missing fundamental packages (required: bisect, collections, os, sys, glob, logging, time, webbrowser).")

try:
    import config as cfg
except:
    print("ImportERROR: Cannot find Hy2Opt.pypool.config")

try:
    from osgeo import ogr
except:
    print("ImportWARNING: Cannot find osgeo.ogr - geospatial functions are not be available.")


# FUNCTION WRAPPERS - MUST BE ON TOP OF THE FILE
def ogr_shp_env(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print("ERROR: osgeo.ogr not available.")
    return wrapper


# MAIN FUNCTIONS
def chk_is_empty(variable):
    try:
        value = float(variable)
    except ValueError:
        value = variable
        pass
    try:
        value = str(variable)
    except ValueError:
        pass
    return bool(value)


def chk_dir(directory):
    # returns False if the directory did not exist yet
    if not os.path.exists(directory):
        os.makedirs(directory)
        return False
    else:
        return True


def clean_dir(directory):
    """
    Delete everything reachable IN the directory named in 'directory',
    assuming there are no symbolic links.
    CAUTION:  This is dangerous!  For example, if directory == '/', it
    could delete all your disk files.
    """
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def copy_tree(source_directory, target_directory):
    """
    Copies all files and folder from source_directory to target directory
    :param source_directory: STR of full path of source directory - must END WITH "/"
    :param target_directory: STR of full path of target directory - must END WITH "/"
    :return: BOOL: False if new model, True if model already exists
    """
    exists = chk_dir(target_directory)
    for dirpath, dirnames, filenames in os.walk(source_directory):
        structure = os.path.join(target_directory, dirpath[len(source_directory):])
        if not os.path.isdir(structure):
            os.mkdir(structure)
        else:
            print("Manual overwrite?")
    return exists


def cool_down(seconds):
    # Pauses script execution for the input argument number of seconds
    # seconds = INT
    sys.stdout.write('Cooling down (waiting for processes to end) ... ')
    for i in range(seconds, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\n')


def del_ovr_files(directory):
    # directory must end with "\\" or "/"
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for f in all_files:
        if ".ovr" in f:
            try:
                print("Attempting to remove old temporary files ...")
                os.remove(directory + f)
                print("Success.")
            except:
                pass


def dict_values2list(dv):
    # converts a 'dict_values' object into a 'list'
    # also works for 'dict_keys' to 'list' conversion
    out_list = []
    [out_list.append(item) for item in dv]
    return out_list


def dict2str(dictionary, **kwargs):
    # converts a dict to a STR expression - reutrn "{e: 1, f: 2, ...}" - used in arcpy-calculatefiel mgmt
    inverse_dict = False  # optional keyword arg: if true: dictionary keys and values will be inversed
    try:
        for k in kwargs.items():
            if "inverse_dict" in k[0]:
                inverse_dict = k[1]
    except:
        pass
    dict_str = "{"
    cc = 1
    for k, v in dictionary.items():
        skey = "\'%s\'" % k if type(k) == str else str(k)
        sval = "\'%s\'" % v if type(v) == str else str(v)
        if not inverse_dict:
            dict_str += "{0}: {1}".format(skey, sval)
        else:
            dict_str += "{1}: {0}".format(skey, sval)
        if not (cc == dictionary.__len__()):
            dict_str += ", "
        else:
            dict_str += "}"
        cc += 1
    return dict_str


def dict_read_from_file(filename, sep=","):
    with open(filename, "r") as f:
        dictionary = {}
        for line in f:
            values = line.split(sep)
            dictionary[values[0]] = {int(x) for x in values[1:len(values)]}
        return dictionary


def dict_nested_read_from_file(filename, sep="::"):
    dictionary = {}
    with open(filename, "r") as f:
        for line in f:
            values = line.strip("\n").split(sep)
            try:
                dictionary[values[0]].update({values[1]: values[2]})
            except KeyError:
                dictionary.update({values[0]: {values[1]: values[2]}})
    try:
        del dictionary[0]  # remove none element if exists
    except KeyError:
        pass
    return dictionary


def dict_write2file(dictionary, filename, sep=","):
    with open(filename, "a") as f:
        for i in dictionary.keys():
            f.write(str(i) + " " + sep.join([str(x) for x in dictionary[i]]) + "\n")


def dict_nested_write2file(dictionary, filename, sep="::"):
    """
    Saves a nested dictionary to filename
    :param dictionary: dict[dict]
    :param filename: STR
    :param sep: STR (optional)
    """
    with open(filename, "w") as f:
        for top_key, sub_dict in dictionary.items():
            for sub_key, sub_val in sub_dict.items():
                f.write(str(top_key) + sep + str(sub_key) + sep + str(sub_val) + "\n")


def file_names_in_dir(directory):
    # returns file names only (without directory)
    return [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def get_closest_val_in_list(usr_list, target_num):
    """ Returns closes value to target_num in a sorted usr_list
    if two numbers are equally close the smallest number is returned
    """
    pos = bisect_left(usr_list, target_num)
    if pos == 0:
        return usr_list[0]
    if pos == len(usr_list):
        return usr_list[-1]
    before = usr_list[pos - 1]
    after = usr_list[pos]
    if after - target_num < target_num - before:
       return after
    else:
       return before


def get_credits():
    c_file = open(cfg.dir2templates + "dialogues/credits.txt", "r")
    credits_str = "\n".join(c_file.read().splitlines())
    c_file.close()
    return credits_str


def get_newest_file(directory, exclude=None):
    """
    Finds the newest file name, excluding those that contain an "exclude" expression
    :param directory: STR of directory
    :param exclude: STR of filetypes to exclude, e.g., ".txt"
    :return: STR of newest file names
    """
    file_list = sorted(glob.iglob(os.path.join(directory, '*')), key=os.path.getctime, reverse=True)
    if exclude:
        for i in file_list:
            if str(exclude) in str(i):
                file_list.remove(i)

    return file_list[0]


@ogr_shp_env
def get_shp_extent(dir2shp):
    """
    Assesses extents of a shapefile using osgeo's ogr module
    :param dir2shp: STR of full path to shapefile (e.g., D:/a_shapefile.shp)
    :return: TUPLE of shapefile extents (INT(X_length[West-East], INT(Y_length[South-North])
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_src = driver.Open(dir2shp, 0)
    layer = data_src.GetLayer()
    x_min, x_max, y_min, y_max = layer.GetExtent()  # returns TUPLE of shapefile extents (Xmin[West], Xmax[East], Ymin[South], Ymax[North])
    grid_size = (round(abs(x_max-x_min)+0.4999), round(abs(y_max - y_min)+0.4999))
    return grid_size


@ogr_shp_env
def get_shp_field_names(dir2shp):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_src = driver.Open(dir2shp, 0)
    layer = data_src.GetLayer()
    ldefn = layer.GetLayerDefn()
    field_names = []
    [field_names.append(ldefn.GetFieldDefn(n).name) for n in range(ldefn.GetFieldCount())]
    return field_names


@ogr_shp_env
def get_shp_field_values(dir2shp, field_name):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_src = driver.Open(dir2shp, 0)
    layer = data_src.GetLayer()
    field_values = []
    [field_values.append(feat.GetField(field_name)) for feat in layer]
    return field_values


def get_subdir_names(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]


def get_tf_models():
    # returns LIST of (internal) Hy2Opt.Tuflow model names
    models = []
    [models.append(f.split("\\")[-1].split("/")[-1].split(".hy2model")[0]) for f in list_file_type_in_dir(cfg.dir2tf + "models/", ".hy2model")]
    if models.__len__() < 1:
        models = ["NO MODEL AVAILABLE"]
    return models


def interpolate_linear(x1, x2, y1, y2, xi):
    # returns linear interpolation yi of xi between two points 1 and 2
    return y1 + ((xi - x1) / (x2 - x1) * (y2 - y1))


def list_file_type_in_dir(directory, f_ending):
    """
    :param directory: full directory ending on "/" or "\\"
    :param f_ending: STR, e.g., ".py"
    :return: LIST of full file paths"""
    return glob.glob(directory + "*" + f_ending)


def open_folder(directory):
    try:
        import subprocess
        # other python versions than 2.7: import subprocess32
        my_platform = sys.platform
        if my_platform[0:3].lower() == "win":
            # print("Hello Windows!")
            call_target = "explorer " + directory
            subprocess.call(call_target, shell=True)
            print("Found subprocess --> opening target folder.")
        if my_platform[0:3].lower() == "lin":
            # print("Hello Linux!")
            subprocess.check_call(['xdg-open', '--', directory])
            print("Found subprocess --> opening target folder.")
        if my_platform[0:3].lower() == "dar":
            # print("Hello Mac OS!")
            subprocess.check_call(['open', '--', directory])
            print("Found subprocess --> opening target folder.")
            try:
                os.system("start \"\" https://en.wikipedia.org/wiki/Criticism_of_Apple_Inc.")
            except:
                pass
    except:
        pass


def print_dict(dictionary):
    out_str = ""
    for k, v in dictionary.items():
        out_str += "   {0} - {1}".format(str(k), str(" + ".join(v)))
    return out_str


def read_file_content(file_path):
    """
    :param file_path: STR of absolute dir to file, including file ending
    :return: list_of_lines: LIST of lines contained in file_path
    """
    list_of_lines = []
    if os.path.isfile(file_path):
        file = open(file_path)
        lines = file.readlines()
        try:
            [list_of_lines.append(l) for l in lines]
        except:
            file.close()
            print("WARNING: Could not read dialogue file (%s)." % file_path)
            return []
        file.close()
    else:
        print("WARNING: Dialogue file (%s) does not exist." % file_path)
        return []
    return list_of_lines


def rm_dir(directory):
    """
    Deletes everything reachable from the directory named in 'directory', and the directory itself
    Assuming there are no symbolic links.
    CAUTION:  This is dangerous!  For example, if directory == '/' deletes all disk files
    """
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(directory)


def rm_file(full_name):
    # fullname = str of directory + file name
    try:
        os.remove(full_name)
    except:
        pass


def str2frac(arg):
    arg = arg.split('/')
    return int(arg[0]) / int(arg[1])


def str2num(arg, sep):
    # function converts string of type 'X[sep]Y' to number
    # sep is either ',' or '.'
    # e.g. '2,30' is converted with SEP = ',' to 2.3
    _num = arg.split(sep)
    _a = int(_num[0])
    _b = int(_num[1])
    _num = _a + _b * 10 ** (-1 * len(str(_b)))
    return _num


def str2tuple(arg):
    try:
        arg = arg.split(',')
        tt = (int(arg[0]), int(arg[1]))
        return tt
    except ValueError:
        print('ERROR: Bad assignment of separator.\nSeparator must be [,].')
        return arg


def tuple2num(arg):
    # function converts float number with ',' separator for digits to '.' separator
    # type(arg) = tuple with two entries, e.g. (2,40)
    # call: tuple2num((2,3))
    new = arg[0] + arg[1] * 10 ** (-1 * len(str(arg[1])))
    return new


def write_data2file(folder_dir, file_name, data):
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    os.chdir(folder_dir)

    f = open(file_name+'.txt', 'w')
    for i in data:
        line = str(i)+'\n'
        f.write(line)
    print('Data written to: \n' + folder_dir + '\\' + str(file_name) + '.txt')

