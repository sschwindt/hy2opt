try:
    import cFrameCtrl as cFC
    from config import *
    import config as cfg
except:
    print("ExceptionERROR: Cannot find pool.")


class Tab(tk.Frame):
    def __init__(self, tab_name=str(), master=None):
        # Construct the Frame object.
        tk.Frame.__init__(self, master)
        # if imported from master GUI, redefine master as highest level (ttk.Notebook tab container)
        if __name__ != '__main__':
            self.master = self.winfo_toplevel()
        self.pack(expand=True, fill=tk.BOTH)

        self.dir2model = '.'
        self.model_name = tk.StringVar()
        self.title = ""
        # tk.Label(text="").grid(row=0, column=0)
        self.furnish(tab_name)
        self.b_return = tk.Button(self, fg="RoyalBlue3", bg="white", text="RETURN to MAIN WINDOW",
                                  command=lambda: self.master.destroy())
        self.b_return.grid(sticky=tk.E, row=25, column=25, columnspan=2, padx=cfg.xd, pady=cfg.yd)

    def furnish(self, parameter):
        """
        Directs to window constructor as a function of a parameter
        :param parameter: STR; either "Model Control", "Geometry", or "Boundary Conditions (Events)"
        :return: None
        """
        if parameter == "Model Control":
            self.furnish_model_ctrl()
        if parameter == "Geometry":
            self.furnish_geometry()
        if parameter == "Boundary Conditions (Events)":
            self.furnish_bc_events()

    def furnish_bc_events(self):
        # make frames for control, stability and output parameters and place frames
        tk.Label(self, text="Model name: ").grid(sticky=tk.W, row=0, column=0, padx=cfg.xd, pady=cfg.yd)
        self.e_name = tk.Entry(self, textvariable=self.model_name)
        self.e_name.grid(sticky=tk.EW, row=0, column=1, columnspan=2, padx=cfg.xd, pady=cfg.yd)


    def furnish_geometry(self):
        tk.Label(self, text="Geometry").grid(sticky=tk.W, row=0, column=0, padx=cfg.xd, pady=cfg.yd)

    def furnish_model_ctrl(self):
        # set control file inquiries
        ctrl_frame = cFC.ControlMaker("ctrl", self, relief=tk.RAISED)
        stab_frame = cFC.ControlMaker("stab", self, relief=tk.RAISED)
        out_frame = cFC.ControlMaker("out", self, relief=tk.RAISED)
        ctrl_frame.grid(sticky=tk.EW, row=0, column=0, columnspan=3, pady=cfg.yd)
        stab_frame.grid(sticky=tk.EW, row=1, column=0, columnspan=3, pady=cfg.yd)
        out_frame.grid(sticky=tk.EW, row=2, column=0, columnspan=3, pady=cfg.yd)



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
        wx = (self.master.winfo_screenwidth() - cfg.ww) / 2
        wy = (self.master.winfo_screenheight() - cfg.wh) / 2
        # Set the height and location.
        self.master.geometry("%dx%d+%d+%d" % (cfg.ww, cfg.wh, wx, wy))
        self.furnish(tab_title)
        # Give the window a title.
        if __name__ == '__main__':
            self.master.title(tab_title)
            self.master.iconbitmap(cfg.code_icon)

    def __call__(self):
        self.mainloop()


class MasterWindow(object):
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        self.top.iconbitmap(cfg.code_icon)

        # ARRANGE GEOMETRY
        wx = (self.top.winfo_screenwidth() - cfg.ww) / 2
        wy = (self.top.winfo_screenheight() - cfg.wh) / 2
        self.top.geometry("%dx%d+%d+%d" % (cfg.ww, cfg.wh, wx, wy))
        self.top.title("Tuflow Model Setup Wizard")  # window title
        self.top.lift()
        self.top.attributes("-topmost", True)
        # self.mbar = tk.Menu(top)
        # self.top.config(menu=self.mbar)
        # self.c_menu = tk.Menu(self.mbar, tearoff=0)
        # self.mbar.add_cascade(label="RETURN", menu=self.c_menu)  # attach it to the menubar
        # self.c_menu.add_command(label="RETURN TO MAIN WINDOW", command=partial(self.top.destroy))


        self.tab_container = ttk.Notebook(self.top)

        self.tab_names = ['Model Control', 'Geometry', 'Boundary Conditions (Events)']
        # self.tabs = {}
        # for tn in self.tab_names:
        #     self.tabs.update({tn: Tab()})
        #     self.tabs[tn].set_geometry(tn)
        # frames initialized by module, with parent being tab container
        self.tab_list = []
        for tn in self.tab_names:
            self.tab_list.append(Tab(tn, self.tab_container))
        #     self.active_tabs[-1].set_geometry(tn)
        # self.tab_list = [Tab(self.tab_container),
        #                  Tab(self.tab_container),
        #                  Tab(self.tab_container)]

        self.tabs = dict(zip(self.tab_names, self.tab_list))

        for tab_name in self.tab_names:
            tab = self.tabs[tab_name]
            tab.bind('<Visibility>', self.tab_select)
            self.tab_container.add(tab, text=tab_name)
            self.tab_container.pack(expand=1, fill="both")

        # # MANDATORY INPUTS FRAME
        # self.mandatory = MandatoryFrame(self.top, relief=tk.RAISED)
        # self.mandatory.grid(row=2, column=0, columnspan=3)
        # self.mandatory.b_info.config(command=lambda: self.select())
        #
        # # OPTIONAL INPUTS FRAME
        # self.optional = OptionalFrame(self.top, relief=tk.RAISED)
        # self.optional.config(bg="khaki")
        # self.optional.grid(row=3, column=0, columnspan=3)


    # def gui_quit(self):
    #     # self.tab_container.destroy()
    #     self.top.destroy()

    def tab_select(self, event):
        selected_tab_name = self.tab_container.tab(self.tab_container.select(), 'text')
        selected_tab = self.tabs[selected_tab_name]
        selected_tab.set_geometry(selected_tab.title)
        # selected_tab.b_return.config(command=self.top.destroy())

    def __call__(self, *args, **kwargs):
        self.top.mainloop()
