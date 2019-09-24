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
        self.config(width=ww, height=int(20 * self.mbce.default_dicts[self.sn].keys().__len__()), bg=self.bg_color)
        tk.Label(self, text=self.mbce.bce_name_dict[self.sn].upper()).grid(sticky=tk.W, row=0, column=0, columnspan=3, padx=xd, pady=yd)

        usr_msg, fg_col = self.chk_model()
        self.l_model_check = tk.Label(self, fg=fg_col, width=100, text=usr_msg)
        self.l_model_check.grid(sticky=tk.W, row=1, column=0, columnspan=3, padx=xd, pady=yd)

        self.make_table()

        self.add()
        self.make_up()

    def add(self):
        # add additional entries as a function of bce-setion names
        if self.sn == "bce":
            pass

    def chk_model(self):
        if not (self.mbce.name == "default"):
            msg0 = "Define events for boundary source areas (define in Name-field of 2d_sa_MODEL_QT_R.shp).\n"
            self.mbce.get_boundary_sa_names()
            msg1 = str("Identified source area names: " + ", ".join(self.mbce.bc_list))
            return msg0 + msg1, "forest green"
        else:
            msg0 = "NOT AVAILABLE\n\nDefine and select a model.\n"
            msg1 = "Event definitions require the prior definition of a mode with a 2d_sa_MODEL_QT_R.shp file (Geometry Tab)."
            return msg0 + msg1, "red3"

    def make_table(self):
        data = {"Model": {}}
        for col_name in self.mbce.bc_list:
            data["Model"].update({col_name: 0.0})

        self.table_frame = Frame(self, width=700)
        self.table_frame.grid(sticky=tk.EW, row=2, column=0, columnspan=3, padx=xd, pady=yd)
        table = TableCanvas(self.table_frame, data=data)
        table.show()

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
