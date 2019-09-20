try:
    from config import *
except:
    print("ImportERROR: Cannot find pool.")


class PopUpT(object):
    def __init__(self, cell_size, master):
        self.top = tk.Toplevel(master)
        self.top.iconbitmap(code_icon)
        msg0 = "The timestep (in seconds) depends on the cell size and should be max. 1/2 to 1/5 of the cell size in meters.\n"
        msg1 = "The timestep must be small enough to satisfy the Courant-Friedrichs-Lewy condition for numerical stability.\n\n"

        self.ts_value = tk.StringVar()
        self.ts = float()

        # inquire Cell Size
        self.cs = tk.StringVar()
        self.cs.set(cell_size)
        tk.Label(self.top, text=msg0 + msg1).grid(sticky=tk.EW, row=0, column=0, columnspan=2, pady=yd)
        tk.Label(self.top, text="Cell size (in METERS):").grid(sticky=tk.W, row=1, column=0, pady=yd)
        self.e_cs = tk.Entry(self.top, width=30, textvariable=self.cs)
        self.e_cs.grid(sticky=tk.W, row=1, column=1, pady=yd)

        # inquire water depth
        self.h = tk.StringVar()
        self.h.set(3.0)
        tk.Label(self.top, text="Estimated water depth (in METERS):").grid(sticky=tk.W, row=2, column=0, pady=yd)
        self.e_h = tk.Entry(self.top, width=30, textvariable=self.h)
        self.e_h.grid(sticky=tk.W, row=2, column=1, pady=yd)

        b_calc = tk.Button(self.top, text="Calculate initial Timestep according to Courant-Friedrichs-Lewy condition",
                           bg="white", command=lambda: self.calc_dt())
        b_calc.grid(sticky=tk.EW, row=3, column=0, columnspan=2, padx=xd, pady=yd)
        self.l_ts = tk.Label(self.top, text="Estimated minimum timestep: ")
        self.l_ts.grid(sticky=tk.W, row=4, column=0, columnspan=2, pady=yd)
        b_calc = tk.Button(self.top, text="Use calculated Timestep and return to main window",
                           fg="RoyalBlue3", bg="white", command=lambda: self.cleanup())
        b_calc.grid(sticky=tk.EW, row=5, column=0, columnspan=2, padx=xd, pady=yd)

    def calc_dt(self):
        self.ts_value.set(float(self.cs.get()) / ((2 * 9.81 * float(self.h.get())) ** (1 / 2)))
        self.l_ts.config(text="Estimated minimum timestep: %s" % str(self.ts_value.get()))

    def cleanup(self):
        self.ts = float(self.ts_value.get())
        self.top.destroy()
