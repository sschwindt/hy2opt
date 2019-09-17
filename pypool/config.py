try:
    import os, sys
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys).")


def set_directories():
    """ Append relevant directories to system path"""
    mdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/"
    for sdir in os.listdir(mdir):
        if os.path.isdir(os.path.join(mdir, sdir)) and not(('idea' in sdir) or ('__' in sdir)):
            print('Appending import folder %s ...' % sdir)
            sys.path.append(os.path.join(mdir, sdir))

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.messagebox import askokcancel, showinfo
    from tkinter.filedialog import *
    import webbrowser
except:
    print("ERROR: Missing package: tkinter.")
try:
    from cLogger import Logger
except:
    print("ERROR: Could not import Logger.")
try:
    import pyhi
except:
    print("ERROR: Could not import Welcome tab.")
try:
    import tuflow
except:
    print("ERROR: Could not import Tuflow tab.")
try:
    import other
except:
    print("ERROR: Could not import Other tab.")


dir2dialogues = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/pyorigin/dialogues/"
dir2master = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\"
dir2templates = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/pyorigin/"
dir2tf = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "/tuflow/"
# software_ids = ["tf"]
# software_names = ["Tuflow"]
# software_dict = dict(zip(software_ids, software_names))


# sqft2ac = float(1 / 43560)
# m2ft = 0.3048

# GUI settings
code_icon = dir2master + "pyorigin\\graphics\\icon.ico"
ww = 900
wh = 700
xd = 5
yd = 5

