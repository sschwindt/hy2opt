try:
    from config import *
    from pop_mat import PopUpMat
    import cTFmodel
    from functools import partial
except:
    print("ExceptionERROR: Cannot find pool.")


class GeoMaker(tk.Frame):
    def __init__(self, section_name, master=None, model_name=None, **options):
        """
        Frames parameter section inquiries as listed in cGeo.ModelGeoControl
        :param section_name: STR of section name - must be one of: "gctrl", "gmat", "gbc"
        :param master: tk.Frame-master
        :param options: relief, ...
        """
        Frame.__init__(self, master, **options)
        if not model_name:
            self.mgeo = cTFmodel.Hy2OptModel("default")
        else:
            self.mgeo = cTFmodel.Hy2OptModel(model_name)
            self.mgeo.overwrite_defaults(section_name)
        self.sn = section_name
        self.bg_color = self.mgeo.geo_bg_colors[self.sn]
        self.config(width=ww, height=int(20 * self.mgeo.default_dicts[self.sn].keys().__len__()), bg=self.bg_color)

        self.l_header = tk.Label(self, text=self.mgeo.geo_name_dict[self.sn].upper())
        self.l_header.grid(sticky=tk.W, row=0, column=0, columnspan=3, padx=xd, pady=yd)
        self.ls = []
        row = 1
        self.par_objects = {}  # objects (entries) for parameters with multiple default choices
        self.geo_buttons = {}  # buttons for selecting geodata
        self.par_rows = {}  # enable identification of parameter columns to add additional buttons
        for par in self.mgeo.default_dicts[self.sn].keys():
            self.ls.append(tk.Label(self, text=par))
            self.ls[-1].grid(sticky=tk.W, row=row, column=0, padx=xd, pady=yd)
            self.par_rows.update({par: row})
            self.par_objects.update({par: tk.Entry(self, width=30)})
            if not isinstance(self.mgeo.default_dicts[self.sn][par][0], str):
                if isinstance(self.mgeo.default_dicts[self.sn][par][0], tuple):
                    self.par_objects[par].insert(tk.END, str(self.mgeo.default_dicts[self.sn][par][0]).strip("()"))
                else:
                    self.par_objects[par].insert(tk.END, str(self.mgeo.default_dicts[self.sn][par][0]))
            else:
                self.par_objects[par].insert(tk.END, self.mgeo.default_dicts[self.sn][par][0])
                self.geo_buttons.update(
                    {par: tk.Button(self, text="Select", width=5, command=partial(self.select_file, par))})
                self.geo_buttons[par].grid(sticky=tk.EW, row=row, column=3, padx=xd, pady=yd)
            self.par_objects[par].grid(sticky=tk.E, row=row, column=1, padx=xd, pady=yd)
            tk.Label(self, fg="gray15", text=str(self.mgeo.geo_format_desc[par])).grid(sticky=tk.W, row=row, column=2,
                                                                                       padx=xd, pady=yd)
            row += 1

        self.add()
        self.make_up()

    def add(self):
        # add additional entries as a function of geosection names
        if self.sn == "gctrl":
            self.b_calc_grid = tk.Button(self, text="Calculate from 2d_loc_MODEL_L.shp", command=lambda: self.calc_gridxy())
            self.b_calc_grid.grid(sticky=tk.EW, row=self.par_rows["Grid Size"], column=3, padx=xd, pady=yd)
            self.b_calc_grid["state"] = "disabled"
        if self.sn == "gmat":
            tk.Button(self, text="Create Materials file", command=lambda: self.pop_mat()).grid(sticky=tk.EW,
                                                                                               row=self.par_rows[
                                                                                                   "Read Materials File"],
                                                                                               column=3, padx=xd,
                                                                                               pady=yd)
            tk.Button(self, text="Select Materials file", command=lambda: self.select_file("Read Materials File")).grid(
                sticky=tk.EW, row=self.par_rows["Read Materials File"], column=4, padx=xd, pady=yd)

    @chk_osgeo
    def calc_gridxy(self):
        shp_file = self.par_objects["Read GIS Location"].get()
        if not str(shp_file).endswith(".shp"):
            showinfo("ERROR", "Define shapefile for Read GIS Location first.", parent=self)
        else:
            try:
                self.mgeo.default_dicts["gctrl"]["Grid Size"][0] = fGl.get_shp_extent(shp_file)
                self.par_objects["Grid Size"].delete(0, 'end')
                self.par_objects["Grid Size"].insert(tk.END,
                                                     str(self.mgeo.default_dicts["gctrl"]["Grid Size"][0]).strip("()"))
            except:
                showinfo("ERROR",
                         "Grid Size calculation failed. Verify shapefile for Read GIS Location or enter manually.",
                         parent=self)

    def make_up(self):
        for wid in self.winfo_children():
            try:
                wid.configure(bg=self.bg_color)
            except:
                pass

    def pop_mat(self):
        pop = PopUpMat(self.master)
        self.master.wait_window(pop.top)
        self.mgeo.default_dicts[self.sn]["Read Materials File"][0] = str(pop.mat_file)
        self.select_file("Read Materials File")

    def select_file(self, par):
        f_types = ('All', '*.*')
        if str(self.mgeo.geo_format_desc[par]).endswith(".shp"):
            f_types = ('Shapefiles', '*.shp')
        if "grid" in str(par).lower():
            f_types = ('Raster', '*.asc;*.flt')
        if "materials" in str(par).lower():
            showinfo("Select", "Please select a material file (CSV format).", parent=self)
            f_types = ('Materials', '*.csv')
        self.mgeo.default_dicts[self.sn][par][0] = askopenfilename(initialdir=dir2master,
                                                                   title="Select " + self.mgeo.geo_format_desc[par],
                                                                   filetypes=[f_types], parent=self)
        self.par_objects[par].delete(0, 'end')
        self.par_objects[par].insert(tk.END, str(self.mgeo.default_dicts[self.sn][par][0]))
        if "2d_loc" in self.mgeo.default_dicts[self.sn][par][0]:
            self.b_calc_grid["state"] = "normal"
