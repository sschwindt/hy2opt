try:
    from config import *
    from pop_cfl_time import PopUpT
    import cCtrl
except:
    print("ExceptionERROR: Cannot find pool.")


class ControlMaker(tk.Frame):
    def __init__(self, section_name, master=None, **options):
        """
        Frames parameter section inquiries as listed in cCtrl.ModelControl
        :param section_name: STR of section name - must be one of: "ctrl", "stab", "out", "rst"
        :param master: tk.Frame-master
        :param options: relief, ...
        """
        Frame.__init__(self, master, **options)
        self.mctrl = cCtrl.ModelControl()
        self.sn = section_name
        self.bg_color = self.mctrl.ctrl_bg_colors[self.sn]

        self.config(width=ww, height=int(20*self.mctrl.ctrl_par_dict[self.sn].keys().__len__()),
                    bg=self.bg_color)

        self.l_header = tk.Label(self, text=self.mctrl.ctrl_name_dict[self.sn].upper())
        self.l_header.grid(sticky=tk.W, row=0, column=0, columnspan=3, padx=xd, pady=yd)
        self.ls = []
        row = 1
        self.par_objects = {}  # objects (comboboxes and entries) for parameters with multiple default choices
        self.par_rows = {}  # enable identification of parameter columns to add additional buttons
        for par in self.mctrl.ctrl_par_dict[self.sn].keys():
            self.ls.append(tk.Label(self, text=par))
            self.ls[-1].grid(sticky=tk.W, row=row, column=0, padx=xd, pady=yd)
            self.par_rows.update({par: row})
            if self.mctrl.ctrl_par_dict[self.sn][par].__len__() > 1:
                self.par_objects.update({par: ttk.Combobox(self, width=30)})
                self.par_objects[par]['state'] = 'readonly'
                self.par_objects[par]['values'] = self.mctrl.ctrl_par_dict[self.sn][par]
                self.par_objects[par].set(self.mctrl.ctrl_par_dict[self.sn][par][0])
            else:
                self.par_objects.update({par: tk.Entry(self, width=30)})
                self.par_objects[par].insert(tk.END, self.mctrl.ctrl_par_dict[self.sn][par][0])
            self.par_objects[par].grid(sticky=tk.E, row=row, column=1, padx=xd, pady=yd)
            row += 1

        self.add()
        self.make_up()

    def add(self):
        # add additional entries as a function of ctrl-section names
        if self.sn == "stab":
            self.timestep = tk.StringVar()
            self.timestep.set(self.par_objects["Timestep"].get())
            self.par_objects["Timestep"].config(textvariable=self.timestep)
            tk.Button(self, text="Estimate", command=lambda: self.pop_time()).grid(sticky=tk.W, row=self.par_rows["Timestep"], column=2, padx=xd, pady=yd)
        if self.sn == "out":
            self.map_formats = ["ALL"]
            self.map_data_types = {}
            tk.Button(self, text="Add", command=lambda: self.format_add()).grid(sticky=tk.W, row=self.par_rows["Map Output Format"], column=2, padx=xd, pady=yd)
            tk.Button(self, text="Reset formats", command=lambda: self.format_clear(), width=10).grid(sticky=tk.W, row=self.par_rows["Map Output Format"], column=3, padx=xd, pady=yd)
            tk.Label(self, text=" for FORMAT: ").grid(sticky=tk.W, row=self.par_rows["Map Output Data Types"], column=2, padx=xd, pady=yd)
            self.cbx_selected_formats = ttk.Combobox(self, width=10)
            self.cbx_selected_formats.grid(sticky=tk.E, row=self.par_rows["Map Output Data Types"], column=3, padx=xd, pady=yd)
            self.cbx_selected_formats['state'] = 'readonly'
            self.cbx_selected_formats.set("ALL")
            tk.Button(self, text="Add", command=lambda: self.format_data_type_add()).grid(sticky=tk.W, row=self.par_rows["Map Output Data Types"], column=4, padx=xd, pady=yd)
            tk.Button(self, text="Reset", command=lambda: self.format_data_type_clear()).grid(sticky=tk.W, row=self.par_rows["Map Output Data Types"], column=5, padx=xd, pady=yd)

    def format_add(self):
        if not (self.par_objects["Map Output Format"].get() in self.map_formats):
            self.map_formats.append(str(self.par_objects["Map Output Format"].get()))
            self.cbx_selected_formats['values'] = self.map_formats
        msg1 = "\nAll currently selected: " + ", ".join(self.map_formats)
        showinfo("Info", str("Added map format: %s " % str(self.par_objects["Map Output Format"].get())) + msg1, parent=self)

    def format_clear(self):
        self.map_formats = ["ALL"]
        self.cbx_selected_formats['values'] = ["ALL"] + self.map_formats
        showinfo("Info", "All map formats cleared. Add at least one.", parent=self)

    def format_data_type_add(self):
        if not (str(self.cbx_selected_formats.get()) in self.map_data_types.keys()):
            self.map_data_types.update({str(self.cbx_selected_formats.get()): [str(self.par_objects["Map Output Data Types"].get())]})
        else:
            self.map_data_types[str(self.cbx_selected_formats.get())].append(str(self.par_objects["Map Output Data Types"].get()))
        info_str = fGl.print_dict(self.map_data_types)
        showinfo("Info", "Currently defined map output data types:\n" + info_str, parent=self)

    def format_data_type_clear(self):
        self.map_data_types = {}
        showinfo("Info", "All map output data types cleared. Add at least one.", parent=self)

    def make_up(self):
        for wid in self.winfo_children():
            try:
                wid.configure(bg=self.bg_color)
            except:
                pass

    def pop_time(self):
        pop = PopUpT(self.par_objects["Cell Size"].get(), self.master)
        self.master.wait_window(pop.top)
        self.timestep.set(float(pop.ts))
