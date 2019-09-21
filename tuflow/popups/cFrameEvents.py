try:
    from config import *
    from pop_cfl_time import PopUpT
    import cTFmodel
    from tkintertable import TableCanvas, TableModel
except:
    print("ImportERROR: Cannot find pypool.")


class EventMaker(tk.Frame):
    def __init__(self, section_name, master=None, model_name=None, **options):
        """
        Frames parameter section inquiries as listed in cEvents.ModelEvents
        :param section_name: STR of section name - must be one of: "bce", "..."
        :param master: tk.Frame-master
        :param options: relief, ...
        """
        Frame.__init__(self, master, **options)
        if not model_name:
            self.mbce = cTFmodel.Hy2OptModel("default")
        else:
            self.mbce = cTFmodel.Hy2OptModel(model_name)
            self.mbce.overwrite_defaults(section_name)
        self.sn = section_name
        self.bg_color = self.mbce.bce_bg_colors[self.sn]
        self.config(width=ww, height=int(20 * self.mbce.default_dicts[self.sn].keys().__len__()),
                    bg=self.bg_color)

        tk.Label(self, text=self.mbce.bce_name_dict[self.sn].upper()).grid(sticky=tk.W, row=0, column=0, columnspan=3, padx=xd, pady=yd)
        if not model_name:
            usr_msg = "ERROR\n\nDefine and select a model. The definition of events requires the prior definition of a mode with a 2d_loc_MODEL_L.shp file (Geometry Tab)."
        else:
            usr_msg = self.mbce.get_boundary_sa_names(model_name)

        ### IMPLEMENT LOAD FUNCTION TO SHOW THIS
        # showinfo("INFO", usr_msg, parent=self)

        ### ADD tkintertable HERE (siehe spielwiese 1)

        # OLD -----------------
        self.ls = []
        row = 1
        self.par_objects = {}  # objects (comboboxes and entries) for parameters with multiple default choices
        self.par_rows = {}  # enable identification of parameter columns to add additional buttons
        for par in self.mbce.default_dicts[self.sn].keys():
            pass
            row += 1

        self.add()
        self.make_up()

    def add(self):
        # add additional entries as a function of bce-setion names
        if self.sn == "bce":
            pass


    def make_up(self):
        for wid in self.winfo_children():
            try:
                wid.configure(bg=self.bg_color)
            except:
                pass

    # def pop_sth(self):
    #     pop = PopUpT(self.par_objects["Cell Size"].get(), self.master)
    #     self.master.wait_window(pop.top)
    #     self.timestep.set(float(pop.ts))
