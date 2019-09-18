try:
    import cFrameCtrl as cFC
    import cTFmodel as cTm
    from config import *
except:
    print("ImportERROR: Cannot find pool.")


class Tab(tk.Frame):
    def __init__(self, tab_name=str(), master=None):
        # tab_name = STR of parameter group for self.furnish()
        tk.Frame.__init__(self, master)
        # if imported from master GUI, redefine master as highest level (ttk.Notebook tab container)
        if __name__ != '__main__':
            self.master = self.winfo_toplevel()
        self.pack(expand=True, fill=tk.BOTH)
        self.model = cTm.Hy2OptModel("default")
        self.changes_saved = False

        self.dir2model = '.'
        self.frame_dict = {}
        self.model_name = tk.StringVar()
        self.title = ""
        self.furnish(tab_name)
        self.b_save = tk.Button(self, fg="red3", bg="white", text="Save Model", command=lambda: self.save_model())
        self.b_save.grid(sticky=tk.EW, row=25, column=0, columnspan=3, padx=xd, pady=yd)
        self.b_return = tk.Button(self, fg="RoyalBlue3", bg="white", text="RETURN to MAIN WINDOW", command=lambda: self.quit_wizard())
        self.b_return.grid(sticky=tk.E, row=25, column=25, padx=xd, pady=yd)

    def furnish(self, par_group):
        """
        Directs to window constructor as a function of a parameter
        :param par_group: STR of parameter group ("Model Control", "Geometry", or "Boundary Conditions (Events)")
        :return: None
        """
        if par_group == "Model Control":
            self.furnish_model_ctrl()
        if par_group == "Geometry":
            self.furnish_geometry()
        if par_group == "Boundary Conditions (Events)":
            self.furnish_bc_events()

    def furnish_bc_events(self):
        # make frames for control, stability and output parameters and place frames
        tk.Label(self, text="BC Events").grid(sticky=tk.W, row=0, column=0, padx=xd, pady=yd)

    def furnish_geometry(self):
        tk.Label(self, text="Geometry").grid(sticky=tk.W, row=0, column=0, padx=xd, pady=yd)

    def furnish_model_ctrl(self):
        # set control file inquiries
        tk.Label(self, text="Model name: ", font="Times 11 bold").grid(sticky=tk.E, row=0, column=0, padx=xd, pady=yd)
        self.e_name = tk.Entry(self, textvariable=self.model_name)
        self.e_name.grid(sticky=tk.EW, row=0, column=1, padx=xd, pady=yd)
        tk.Label(self, text=".h2model").grid(sticky=tk.W, row=0, column=2, padx=xd, pady=yd)
        ctrl_frame = cFC.ControlMaker("ctrl", self, relief=tk.RAISED)
        stab_frame = cFC.ControlMaker("stab", self, relief=tk.RAISED)
        out_frame = cFC.ControlMaker("out", self, relief=tk.RAISED)
        ctrl_frame.grid(sticky=tk.EW, row=1, column=0, columnspan=3, pady=yd)
        stab_frame.grid(sticky=tk.EW, row=2, column=0, columnspan=3, pady=yd)
        out_frame.grid(sticky=tk.EW, row=3, column=0, columnspan=3, pady=yd)
        self.frame_dict = {"ctrl": ctrl_frame, "stab": stab_frame, "out": out_frame}

    def quit_wizard(self):
        answer = askyesno("Quit?", "Make sure to SAVE MODEL settings. Return to main window?")
        if answer:
            self.master.destroy()

    def save_model(self):
        self.model.set_model_name(str(self.model_name.get()))
        for par_group, par_frame in self.frame_dict.items():
            for par, val in par_frame.par_objects.items():
                if not (("Map" in par) and (("Format" in par) or ("Data" in par))):
                    self.model.set_usr_parameters(par_group, par, [str(val.get())])
                else:
                    if "Format" in par:
                        self.model.set_usr_parameters(par_group, par, par_frame.map_formats)
                    if "Data" in par:
                        for map_k, map_v in par_frame.map_data_types.items():
                            par_str = str(str(map_k) + " " + par).replace("All ", "")
                            self.model.set_usr_parameters(par_group, par_str, map_v)
        self.changes_saved = True
        self.b_save.config(fg="forest green", text="Save Model (last saved: %s)" % str(datetime.datetime.now()))

    @staticmethod
    def set_bg_color(master_frame, bg_color):
        master_frame.config(bg=bg_color)
        for wid in master_frame.winfo_children():
            try:
                wid.configure(bg=bg_color)
            except:
                pass  # some widget do not accept bg as kwarg

    def set_geometry(self, tab_title):
        # ww and wh = INT of window width and window height
        # Upper-left corner of the window.
        self.title = tab_title
        wx = (self.master.winfo_screenwidth() - ww) / 2
        wy = (self.master.winfo_screenheight() - wh) / 2
        # Set the height and location.
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
        self.furnish(tab_title)
        # Give the window a title.
        if __name__ == '__main__':
            self.master.title(tab_title)
            self.master.iconbitmap(code_icon)

    def __call__(self):
        self.mainloop()


class MasterWindow(object):
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.iconbitmap(code_icon)

        # ARRANGE GEOMETRY
        wx = (self.top.winfo_screenwidth() - ww) / 2
        wy = (self.top.winfo_screenheight() - wh) / 2
        self.top.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
        self.top.title("Tuflow Model Setup Wizard")  # window title
        self.top.lift()
        # self.top.attributes("-topmost", True)
        # self.mbar = tk.Menu(top)
        # self.top.config(menu=self.mbar)
        # self.c_menu = tk.Menu(self.mbar, tearoff=0)
        # self.mbar.add_cascade(label="RETURN", menu=self.c_menu)  # attach it to the menubar
        # self.c_menu.add_command(label="RETURN TO MAIN WINDOW", command=partial(self.top.destroy))

        self.tab_container = ttk.Notebook(self.top)
        self.tab_names = ['Model Control', 'Geometry', 'Boundary Conditions (Events)']
        self.tab_list = []
        for tn in self.tab_names:
            self.tab_list.append(Tab(tn, self.tab_container))

        self.tabs = dict(zip(self.tab_names, self.tab_list))

        for tab_name in self.tab_names:
            tab = self.tabs[tab_name]
            tab.bind('<Visibility>', self.tab_select)
            self.tab_container.add(tab, text=tab_name)
            self.tab_container.pack(expand=1, fill="both")

    def tab_select(self, event):
        selected_tab_name = self.tab_container.tab(self.tab_container.select(), 'text')
        selected_tab = self.tabs[selected_tab_name]
        selected_tab.set_geometry(selected_tab.title)
        if (str(selected_tab.model_name.get()).__len__() > 1) and not(selected_tab.changes_saved):
            askokcancel("Save", "")

    def __call__(self, *args, **kwargs):
        self.top.mainloop()
