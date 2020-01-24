try:
    from tabs import *
except:
    print("ExceptionERROR: Cannot find package files (pool).")


class OtherTab(ModuleTab):
    def __init__(self, from_master):
        ModuleTab.__init__(self, from_master)
        self.title = "Other"
        self.set_geometry(self.title)

        # GUI OBJECT VARIABLES
        self.gui_interpreter = tk.StringVar()
        self.l_hello = tk.Label(self, text="Other model")
        self.l_hello.grid(sticky=tk.W, row=0, column=0, padx=cfg.xd, pady=cfg.yd)

        # self.c_interp = ttk.Combobox(self, width=30)
        # self.c_interp.grid(sticky=tk.W, row=0, column=1, padx=cfg.xd, pady=cfg.yd)
        # self.c_interp['state'] = 'readonly'
        # self.c_interp['values'] = self.get_models()
        # self.c_interp.set(" -- SELECT -- ")
        # self.b_create = tk.Button(self, bg="white", text="Apply selection", command=lambda: self.validate_selection())
        # self.b_create.grid(sticky=tk.EW, row=0, column=2, padx=cfg.xd, pady=cfg.yd)
        #
        # tk.Label(self, text="Tuflow installation directory:").grid(sticky=tk.W, row=1, column=0, padx=cfg.xd, pady=cfg.yd)
        # self.l_tf = tk.Label(self, text="%s" % self.tf_dir, width=30, justify=tk.LEFT)
        # self.l_tf.grid(sticky=tk.W, row=1, column=1, padx=cfg.xd, pady=cfg.yd)
        # self.b_ch_tf_dir = tk.Button(self, bg="white", text="Change", command=lambda: self.tf_dir_set())
        # self.b_ch_tf_dir.grid(sticky=tk.EW, row=1, rowspan=2, column=2, padx=cfg.xd, pady=cfg.yd)

    def __call__(self):
        self.mainloop()
