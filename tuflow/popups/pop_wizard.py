try:
    import cFrameCtrl as cFC
    import cFrameGeo as cFG
    import cFrameEvents as cFE
    import cTFmodel as cTm
    from config import *
except:
    print("ImportERROR: Cannot find pypool.")


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
        self.title = tab_name
        self.furnish()

        # make common tkinter objects
        tk.Label(self, text="Model name: ", font="Times 11 bold").grid(sticky=tk.E, row=0, column=0, padx=xd, pady=yd)
        self.b_save = tk.Button(self, fg="red3", bg="white", text="Save Model", command=lambda: self.save_model())
        self.b_save.grid(sticky=tk.EW, row=25, column=0, columnspan=3, padx=xd, pady=yd)

        self.b_return = tk.Button(self, fg="RoyalBlue3", bg="white", text="RETURN to MAIN WINDOW", command=lambda: self.quit_wizard())
        self.b_return.grid(sticky=tk.E, row=25, column=25, padx=xd, pady=yd)

    def assign_model_name(self):
        if ("geo" in self.title.lower()) or ("event" in self.title.lower()):
            self.model_name.set(str(self.cbx_model.get()))
            self.model.set_model_name(str(self.cbx_model.get()))

    def furnish(self):
        """
        Directs to window constructor as a function of a parameter
        :param par_group: STR of parameter group ("Model Control", "Geometry", or "Boundary Conditions (Events)")
        :return: None
        """
        if self.title == "Model Control":
            self.furnish_model_ctrl()
        if self.title == "Geometry":
            self.furnish_geometry()
        if self.title == "BC Events":
            self.furnish_bc_events()

    def furnish_bc_events(self):
        # make frames for control, stability and output parameters and place frames
        self.place_model_cbx()
        self.assign_model_name()
        bce_frame = cFE.EventMaker("bce", self, model_name=self.verify_model("bce"), relief=tk.RAISED)
        bce_frame.grid(sticky=tk.EW, row=1, column=0, columnspan=3, pady=yd)
        self.frame_dict = {"bce": bce_frame}

    def furnish_geometry(self):
        self.place_model_cbx()
        self.assign_model_name()
        gctrl_frame = cFG.GeoMaker("gctrl", self, model_name=self.verify_model("gctrl"), relief=tk.RAISED)
        gmat_frame = cFG.GeoMaker("gmat", self, model_name=self.verify_model("gmat"), relief=tk.RAISED)
        gbc_frame = cFG.GeoMaker("gbc", self, model_name=self.verify_model("gbc"), relief=tk.RAISED)
        gctrl_frame.grid(sticky=tk.EW, row=1, column=0, columnspan=3, pady=yd)
        gmat_frame.grid(sticky=tk.EW, row=2, column=0, columnspan=3, pady=yd)
        gbc_frame.grid(sticky=tk.EW, row=3, column=0, columnspan=3, pady=yd)
        self.frame_dict = {"gctrl": gctrl_frame, "gmat": gmat_frame, "gbc": gbc_frame}

    def furnish_model_ctrl(self):
        # set control file inquiries
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

    def place_model_cbx(self, refresh=False):
        if not refresh:
            self.cbx_model = ttk.Combobox(self)
            self.cbx_model.grid(sticky=tk.EW, row=0, column=1, padx=xd, pady=yd)
            tk.Button(self, text="Refresh", command=lambda: self.reload_frames()).grid(sticky=tk.W, row=0, column=2, padx=xd, pady=yd)
        try:
            # necessary because first call will run into emptiness...
            self.cbx_model['state'] = 'readonly'
            self.cbx_model['values'] = fGl.get_tf_models()
        except AttributeError:
            return ""
        try:
            self.cbx_model.set(
                fGl.get_newest_file(dir2tf + "models/", exclude="event").split("\\")[-1].split("/")[-1].split(".hy2model")[0])
        except:
            self.cbx_model.set("NO MODEL AVAILABLE")

    def quit_wizard(self):
        answer = askyesno("Quit?", "Make sure to SAVE MODEL settings. Return to main window?")
        if answer:
            self.master.destroy()

    def reload_frames(self):
        for frame in self.frame_dict.values():
            frame.destroy()
        self.furnish()

    def save_model(self):
        self.assign_model_name()
        try:
            self.model.set_model_name(str(self.model_name.get()))
            for par_group, par_frame in self.frame_dict.items():
                for par, val in par_frame.par_objects.items():
                    if not (("Map" in par) and (("Format" in par) or ("Data" in par)) or ("Events" in par)):
                        self.model.set_usr_parameters(par_group, par, [str(val.get())])
                    else:
                        if "Format" in par:
                            self.model.set_usr_parameters(par_group, par, par_frame.map_formats)
                        if "Data" in par:
                            for map_k, map_v in par_frame.map_data_types.items():
                                par_str = str(str(map_k) + " " + par).replace("All ", "")
                                self.model.set_usr_parameters(par_group, par_str, map_v)
                        if "Events" in par:
                            self.model.set_usr_parameters(par_group, par, val)
                            par_frame.save_event_file()
                self.model.sign_model(par_group)
            self.changes_saved = True
            self.b_save.config(fg="forest green", text="Save Model (last saved: %s)" % str(datetime.datetime.now()).split(".")[0])
        except IndexError:
            showinfo("ERROR", "Could not save model (Map Output Parameters defined?).", parent=self)

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
        wx = int((self.master.winfo_screenwidth() - ww) / 3)
        wy = int((self.master.winfo_screenheight() - wh) / 3)
        # Set the height and location.
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
        self.furnish()
        # Give the window a title.
        if __name__ == '__main__':
            self.master.title(tab_title)
            self.master.iconbitmap(code_icon)

    def verify_model(self, par_group):
        """ Uses model signatures to verify if the par_group was already saved earlier
        :param par_group: STR of parameter group (see cTFmodel.Hy2OptModel)
        :return: STR of model_name if signature=True OR None if signature==False
        """

        if self.model.signature_verification(par_group):
            return str(self.model_name.get())
        else:
            return None

    def __call__(self):
        self.mainloop()


class MasterWindow(object):
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.iconbitmap(code_icon)

        # ARRANGE GEOMETRY
        wx = int((self.top.winfo_screenwidth() - ww) / 3)
        wy = int((self.top.winfo_screenheight() - wh) / 3)
        self.top.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
        self.top.title("Tuflow Model Setup Wizard")  # window title
        self.top.lift()

        self.mbar = tk.Menu(self.top)  # create new menubar
        self.top.config(menu=self.mbar)  # attach it to the root window

        # CLOSE DROP DOWN
        self.gmenu = tk.Menu(self.mbar, tearoff=0)  # create new menu
        self.mbar.add_cascade(label="Generate Model", menu=self.gmenu)  # attach it to the menubar
        self.gmenu.add_command(label="Default", command=lambda: self.generate_model())  # replace with partial function

        self.tab_container = ttk.Notebook(self.top)
        self.tab_names = ['Model Control', 'Geometry', 'BC Events']
        self.tab_list = []
        for tn in self.tab_names:
            self.tab_list.append(Tab(tn, self.tab_container))

        self.tabs = dict(zip(self.tab_names, self.tab_list))

        for tab_name in self.tab_names:
            tab = self.tabs[tab_name]
            tab.bind('<Visibility>', self.tab_select)
            tab.bind("<<NotebookTabChanged>>",
                     lambda event: event.widget.winfo_children()[event.widget.index("current")].update())  # preserve user entries
            self.tab_container.add(tab, text=tab_name)
            self.tab_container.pack(expand=1, fill="both")

    def generate_model(self, model_name=None):
        pass

    def update_model_menu(self):
        pass

    def tab_select(self, event):
        selected_tab_name = self.tab_container.tab(self.tab_container.select(), 'text')
        self.selected_tab = self.tabs[selected_tab_name]
        self.selected_tab.place_model_cbx(refresh=True)
        self.selected_tab.set_geometry(self.selected_tab.title)

    def __call__(self, *args, **kwargs):
        self.top.mainloop()
