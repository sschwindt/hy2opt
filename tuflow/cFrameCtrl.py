try:
    from config import *
    import config as cfg
    import cCtrl
except:
    print("ExceptionERROR: Cannot find pool.")


class ControlMaker(tk.Frame):
    def __init__(self, section_name, master=None, **options):
        """
        Frames parameter section inquiries as listed in cCtrl.ModelControl
        :param section_name: STR of section name - must be oone of: "ctrl", "stab", "out", "rst"
        :param master: tk.Frame-master
        :param options:
        """
        Frame.__init__(self, master, **options)
        self.mctrl = cCtrl.ModelControl()
        self.sn = section_name
        self.bg_color = self.mctrl.section_bg_colors[self.sn]

        self.config(width=cfg.ww, height=int(20*self.mctrl.section_par_dict[self.sn].keys().__len__()),
                    bg=self.bg_color)

        self.l_header = tk.Label(self, text=self.mctrl.section_name_dict[self.sn].upper())
        self.l_header.grid(sticky=tk.EW, row=0, column=0, columnspan=3, padx=cfg.xd, pady=cfg.yd)
        self.ls = []
        row = 1
        self.pars_cbx = {}  # comboboxes for parameters with multiple default choices
        self.pars_ent = {}  # entries for parameters with user-defined str/float
        self.par_rows = {}  # enable identification of parameter columns to add additional buttons
        for par in self.mctrl.section_par_dict[self.sn].keys():
            self.ls.append(tk.Label(self, text=par))
            self.ls[-1].grid(sticky=tk.W, row=row, column=0, padx=cfg.xd, pady=cfg.yd)
            self.par_rows.update({par: row})
            if self.mctrl.section_par_dict[self.sn][par].__len__() > 1:
                self.pars_cbx.update({par: ttk.Combobox(self, width=30)})
                self.pars_cbx[par].grid(sticky=tk.E, row=row, column=1, padx=cfg.xd, pady=cfg.yd)
                self.pars_cbx[par]['state'] = 'readonly'
                self.pars_cbx[par]['values'] = self.mctrl.section_par_dict[self.sn][par]
                self.pars_cbx[par].set(self.mctrl.section_par_dict[self.sn][par][0])
            else:
                self.pars_ent.update({par: tk.Entry(self, width=30)})
                self.pars_ent[par].grid(sticky=tk.E, row=row, column=1, padx=cfg.xd, pady=cfg.yd)
                self.pars_ent[par].insert(tk.END, self.mctrl.section_par_dict[self.sn][par][0])
            row += 1

        self.add()
        self.make_up()

    def add(self):
        # add additional entries as a function of section names
        if self.sn == "stab":
            self.timestep = tk.StringVar()
            self.pars_ent["Timestep"].config(textvariable=self.timestep)
            # tk.Button(text="Estimate", command=lambda: self.pop_time()).grid(sticky=tk.W, row=self.par_rows["Timestep"],
            #                                                                  column=2, padx=cfg.xd, pady=cfg.yd)


    def make_up(self):
        for wid in self.winfo_children():
            try:
                wid.configure(bg=self.bg_color)
            except:
                pass

    def pop_time(self):
        pop = PopUpT(self.pars_ent["Cell Size"].get(), self.master)
        self.master.wait_window(pop.top)
        # self.timestep.set(float(pop.value))


class PopUpT(object):
    def __init__(self, cell_size, master):
        self.top = tk.Toplevel(master)
        msg0 = "The timestep (in seconds) depends on the cell size and should be max. 1/2 to 1/5 of the cell size in meters. \n"
        msg1 = "The timestep must be small enough to satisfy the Courant-Friedrichs-Lewy condition for numerical stability.\n\n"

        self.cs = tk.StringVar()
        self.cs.set(cell_size)
        tk.Label(self.top, text=msg0 + msg1).grid(sticky=tk.EW, row=0, column=0, columnspan=3, pady=cfg.yd)
        tk.Label(self.top, text="The provided cell size is (in Meters!):").grid(sticky=tk.W, row=1, column=0, pady=cfg.yd)
        self.e_cs = tk.Entry(width=30, textvariable=self.cs)
        self.e_cs.grid(sticky=tk.W, row=1, column=1, pady=cfg.yd)

        b_calc = tk.Button(text="Calculate initial Timestep according to Courant-Friedrichs-Lewy condition",
                           command=self.calc_dt)
        b_calc.grid(sticky=tk.EW, row=2, column=0, columnspan=3, pady=cfg.yd)


        self.top.iconbitmap(cfg.code_icon)

    def calc_dt(self):
        dt = float(self.cs.get()) / (9.81 * 10)

    def cleanup(self):
        self.value = self.e_cs.get()
        self.top.destroy()