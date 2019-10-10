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
        self.number_of_events = 1
        self.del_event_var = tk.StringVar()

        self.bg_color = self.mbce.bce_bg_colors[self.sn]
        self.config(width=ww, height=int(20 * self.mbce.default_dicts[self.sn].keys().__len__()), bg=self.bg_color)
        tk.Label(self, text=self.mbce.bce_name_dict[self.sn].upper()).grid(sticky=tk.W, row=0, column=0, columnspan=3, padx=xd, pady=yd)

        usr_msg, fg_col = self.chk_model()
        self.l_model_check = tk.Label(self, fg=fg_col, width=85, text=usr_msg)
        self.l_model_check.grid(sticky=tk.W, row=1, column=0, columnspan=3, padx=xd, pady=yd)

        self.par_objects = {"Events": self.mbce.event_file}
        if os.path.isfile(dir2tf + "models/" + self.mbce.event_file[0]):
            self.mbce.events = fGl.dict_nested_read_from_file(dir2tf + "models/" + self.mbce.event_file[0])

        self.table_frame = Frame(self, width=700)
        self.table_frame.grid(sticky=tk.EW, row=2, rowspan=2, column=0, columnspan=3, padx=xd, pady=yd)
        self.table = TableCanvas(self.table_frame, data=self.mbce.events)
        if model_name:
            self.table.show()

        tk.Button(self, text="Add event", command=lambda: self.add_row()).grid(sticky=tk.EW, row=2, column=3, padx=xd, pady=yd)
        tk.Button(self, text="Delete event\n(row) No:", command=lambda: self.del_row()).grid(sticky=tk.EW, row=3, column=3, padx=xd, pady=yd)
        tk.Entry(self, width=3, textvariable=self.del_event_var).grid(sticky=tk.EW, row=3, column=4, padx=xd, pady=yd)

        self.make_up()

    def add_row(self):
        self.number_of_events += 1
        self.table.addRow(self.number_of_events)

    def del_row(self):
        self.number_of_events -= 1
        try:
            del_row = int(self.del_event_var.get()) - 1
            self.table.setSelectedRow(del_row)
            self.table.deleteRow()
        except:
            showinfo("INFO", "The event number must be a positive integer of a present row number.", parent=self)
            return -1

        if self.number_of_events < 1:
            showinfo("WARNING", "Define at least one event!", parent=self)

    def chk_model(self):
        if not (self.mbce.name == "default"):
            msg0 = "Define flows of boundary source areas (define in Name-field of 2d_sa_MODEL_QT_R.shp).\n"
            self.mbce.get_boundary_sa_names()
            msg1 = str("Identified source area names: " + ", ".join(self.mbce.bc_list))
            return msg0 + msg1, "forest green"
        else:
            msg0 = "NOT AVAILABLE\n\nDefine and select a model.\n"
            msg1 = "Event definitions require the prior definition of a mode with a 2d_sa_MODEL_QT_R.shp file (Geometry Tab)."
            return msg0 + msg1, "red3"

    def make_up(self):
        for wid in self.winfo_children():
            try:
                wid.configure(bg=self.bg_color)
            except:
                pass

    def save_event_file(self):
        self.mbce.events = {}  # reset events dictionary

        for row in range(1, self.table.rows+1):
            self.mbce.events.update({row: {}})
            for col in self.table.model.columnNames:
                try:
                    self.mbce.events[row].update({col: self.table.model.data[row][col]})
                except:
                    print("Setting %s to 0.0 (no value defined)" % str(col))
                    self.mbce.events[row].update({col: 0.0})
            try:
                del self.mbce.events[row][0]  # delete initial non-sense entry
            except:
                pass
        try:
            del self.mbce.events[0]  # delete initial non-sense entry
        except:
            pass

        fGl.dict_nested_write2file(self.mbce.events, dir2tf + "models/" + self.mbce.event_file[0])



        # self.table.save(dir2tf + "models/" + self.mbce.event_file)

    # def pop_sth(self):
    #     pop = PopUpT(self.par_objects["Cell Size"].get(), self.master)
    #     self.master.wait_window(pop.top)
    #     self.timestep.set(float(pop.ts))
