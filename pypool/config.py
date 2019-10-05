try:
    import os, sys, datetime, logging, webbrowser
except:
    print("ImportERROR: Missing fundamental packages (required: os, sys, datetime, logging, webbrowser).")
try:
    import fGlobal as fGl
except:
    print("ImportERROR: Could not import pypool.fGlobal")
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.messagebox import askokcancel, showinfo, askyesno
    from tkinter.filedialog import *
except:
    print("ImportERROR: Missing package: tkinter.")
try:
    from cLogger import Logger
except:
    print("ImportERROR: Could not import pypool.cLogger.Logger")
try:
    import pyhi
except:
    print("ImportERROR: Could not import .pyhi")
try:
    import tuflow
except:
    print("ImportERROR: Could not import .tuflow")
try:
    import other
except:
    print("ImportERROR: Could not import .other")


def set_directories():
    """ Append relevant directories to system path"""
    mdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/"
    for sdir in os.listdir(mdir):
        if os.path.isdir(os.path.join(mdir, sdir)) and not(('idea' in sdir) or ('__' in sdir)):
            print('Appending import folder %s ...' % sdir)
            sys.path.append(os.path.join(mdir, sdir))


def chk_osgeo(func):
    def wrapper(*args, **kwargs):
        try:
            from osgeo import ogr
            func(*args, **kwargs)
        except ModuleNotFoundError:
            showinfo("ERROR", "Install osgeo.ogr to enable this Hy2Opt feature.")
        except ImportError:
            showinfo("ERROR", "Install osgeo.ogr to enable this Hy2Opt feature.")
    return wrapper


def log_actions(func):
    def wrapper(*args, **kwargs):
        logger = Logger("logfile")
        func(*args, **kwargs)
        logger.logging_stop()
    return wrapper

dir2dialogues = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/pyorigin/dialogues/"
dir2master = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\"
dir2templates = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/pyorigin/"
dir2tf = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tuflow/"
# software_ids = ["tf"]
# software_names = ["Tuflow"]
# software_dict = dict(zip(software_ids, software_names))
tf_source_tree = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/pyorigin/tf_tree/"


# sqft2ac = float(1 / 43560)
# m2ft = 0.3048

# GUI settings
code_icon = dir2master + "pyorigin\\graphics\\icon.ico"
ww = 900
wh = 700
xd = 5
yd = 5

