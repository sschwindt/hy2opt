try:
    from tabs import *
except:
    print("ExceptionERROR: Cannot access pypool files.")


class WelcomeTab(ModuleTab):
    def __init__(self, from_master):
        ModuleTab.__init__(self, from_master)
        self.title = "Welcome"
        self.set_geometry(self.title)

        # GUI OBJECT VARIABLES
        self.gui_interpreter = tk.StringVar()
        self.l_hello = tk.Label(self, fg="gray50", text="Toggle through tabs for model setup and initialization")
        self.l_hello.grid(sticky=tk.EW, row=0, column=0, columnspan=2, padx=cfg.xd, pady=cfg.yd)

        # BUTTONS
        # self.b_create_c = tk.Button(self, width=30, bg="white", text="Create New Condition", command=lambda: self.create_c())
        # self.b_create_c.grid(sticky=tk.EW, row=0, column=0, columnspan=2, padx=cfg.xd, pady=cfg.yd*2)

        # MAKE PLACEHOLDER FILL
        logo = tk.PhotoImage(file=os.path.dirname(os.path.abspath(__file__))+"\\welcome.gif")
        logo = logo.subsample(1, 1)
        self.l_img = tk.Label(self, image=logo)
        self.l_img.image = logo
        self.l_img.grid(sticky=tk.E, row=1, column=0)#,  padx=cfg.xd*5, pady=cfg.yd*5)

        # Add credits
        # self.l_credits = tk.Label(self, fg="gray50", text=fGl.get_credits(), justify=LEFT)
        # self.l_credits.grid(sticky=tk.E, row=8, column=1, rowspan=3, columnspan=2, padx=cfg.xd, pady=cfg.yd)

    def __call__(self):
        self.mainloop()
