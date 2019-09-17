try:
    import os, sys
    import tkinter as tk
    from tkinter import ttk
    from tkinter.messagebox import askokcancel, askyesno, showinfo
    from tkinter.filedialog import *
    import webbrowser, logging
except:
    print("ERROR: Missing fundamental packages (required: os, sys, tkinter, webbrowser).")
try:
    import fGlobal as fGl
    import config as cfg
except:
    print("ERROR: Could not import functions.")


class ModuleTab(tk.Frame):
    def __init__(self, master=None):
        self.errors = False
        self.logger = logging.getLogger("logfile")

        # Construct the Frame object.
        tk.Frame.__init__(self, master)
        # if imported from master GUI, redefine master as highest level (ttk.Notebook tab container)
        if __name__ != '__main__':
            self.master = self.winfo_toplevel()
        self.pack(expand=True, fill=tk.BOTH)

    def close_window(self, tk_object):
        # answer = askyesno("Info", "Do you want to close the window?")
        tk_object.destroy()

    def make_standard_menus(self):
        # DROP DOWN MENU
        # the menu does not need packing - see page 44ff
        self.mbar = tk.Menu(self)  # create new menubar
        self.master.config(menu=self.mbar)  # attach it to the root window

        # CLOSE DROP DOWN
        self.closemenu = tk.Menu(self.mbar, tearoff=0)  # create new menu
        self.mbar.add_cascade(label="Close", menu=self.closemenu)  # attach it to the menubar
        self.closemenu.add_command(label="Credits", command=lambda: self.show_credits())
        self.closemenu.add_command(label="Quit program", command=lambda: self.close_window(self.master))

    def refresh_listbox(self, lb, sb, mdir):
        """
        Refreshes ListBox as a function of folder names in mdir
        :param lb: ListBox
        :param sb: ScrollBar
        :param mdir: directory with subfolders
        :return: None
        """
        # lb = tk.ListBox of conditions
        # sb = tk.Scrollbar of conditions
        try:
            lb.delete(0, tk.END)
        except:
            pass

        for e in fGl.get_subdir_names(mdir):
            lb.insert(tk.END, e)
        sb.config(command=lb.yview)

    @staticmethod
    def set_bg_color(master_frame, bg_color):
        master_frame.config(bg=bg_color)
        for wid in master_frame.winfo_children():
            try:
                wid.configure(bg=bg_color)
            except:
                # some widget do not accept bg as kwarg
                pass

    def set_geometry(self, tab_title):
        # ww and wh = INT of window width and window height
        # Upper-left corner of the window.
        wx = (self.master.winfo_screenwidth() - cfg.ww) / 2
        wy = (self.master.winfo_screenheight() - cfg.wh) / 2
        # Set the height and location.
        self.master.geometry("%dx%d+%d+%d" % (cfg.ww, cfg.wh, wx, wy))
        # Give the window a title.
        if __name__ == '__main__':
            self.master.title(tab_title)
            self.master.iconbitmap(cfg.code_icon)

    def show_credits(self):
        showinfo("Credits", fGl.get_credits())
