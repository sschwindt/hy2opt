try:
    from tabs import *
except:
    print("ExceptionERROR: Cannot find package files (pool).")


class TuflowTab(ModuleTab):
    def __init__(self, from_master):
        ModuleTab.__init__(self, from_master)
        self.title = "Tuflow"
        self.set_geometry(self.title)

        self.tf_dir = self.tf_dir_get()

        # GUI OBJECT VARIABLES
        self.gui_interpreter = tk.StringVar()
        self.l_hello = tk.Label(self, text="Select model or create new:")
        self.l_hello.grid(sticky=tk.W, row=0, column=0, padx=cfg.xd, pady=cfg.yd)

        self.c_interp = ttk.Combobox(self, width=30)
        self.c_interp.grid(sticky=tk.W, row=0, column=1, padx=cfg.xd, pady=cfg.yd)
        self.c_interp['state'] = 'readonly'
        self.c_interp['values'] = self.get_models()
        self.c_interp.set(" -- SELECT -- ")
        self.b_create = tk.Button(self, bg="white", text="Apply selection", command=lambda: self.validate_selection())
        self.b_create.grid(sticky=tk.EW, row=0, column=2, padx=cfg.xd, pady=cfg.yd)

        tk.Label(self, text="Tuflow installation directory:").grid(sticky=tk.W, row=1, column=0, padx=cfg.xd, pady=cfg.yd)
        self.l_tf = tk.Label(self, text="%s" % self.tf_dir, width=30, justify=tk.LEFT)
        self.l_tf.grid(sticky=tk.W, row=1, column=1, padx=cfg.xd, pady=cfg.yd)
        self.b_ch_tf_dir = tk.Button(self, bg="white", text="Change", command=lambda: self.tf_dir_set())
        self.b_ch_tf_dir.grid(sticky=tk.EW, row=1, rowspan=2, column=2, padx=cfg.xd, pady=cfg.yd)

    def launch_wizard(self):
        try:
            import popups.pop_wizard as pcw
        except:
            showinfo("Oups ...", "Cannot find Model Setup Wizard -  check installation.")
            return -1
        new_window = pcw.MasterWindow(self.master)
        l_temp = tk.Label(self, fg="gray50", text="WINDOW INACTIVE WHILE EXECUTING WIZARD")
        l_temp.grid(sticky=tk.EW, row=5, column=0, columnspan=3, padx=cfg.xd, pady=cfg.yd)
        self.b_create["state"] = "disabled"
        self.master.wait_window(new_window.top)
        self.b_create["state"] = "normal"
        l_temp.destroy()

    def tf_dir_get(self):
        return str(fGl.read_file_content(cfg.dir2tf + 'settings/tf_dir.def')[0].strip("\n"))

    def tf_dir_set(self):
        self.tf_dir = askdirectory(initialdir=".") + "/"
        if not os.path.isfile(self.tf_dir + 'TUFLOW_iSP_w64.exe') and (str(sys.platform)[0:3].lower() == "win"):
            showinfo("WARNING", "Cannot locate TUFLOW_iSP_w64.exe in the defined directory.")
        f_tf_def = cfg.dir2tf + 'settings/tf_dir.def'
        fGl.rm_file(f_tf_def)  # safely remove existing file
        _f = open(f_tf_def, 'w')
        _f.write(self.tf_dir)
        self.l_tf.config(text="%s" % self.tf_dir)

    def get_models(self):
        model_list = []
        for e in fGl.list_file_type_in_dir(cfg.dir2tf + "models/", ".hy2model"):
            model_list.append(e.split("\\")[-1].split("/")[-1].split(".hy2model")[0])
        return [" -- SELECT -- ", "MODEL SETUP WIZARD"] + model_list

    def validate_selection(self):
        if "wizard" in str(self.c_interp.get()).lower():
            self.launch_wizard()

    def __call__(self):
        self.mainloop()
