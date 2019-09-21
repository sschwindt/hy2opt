try:
    from config import *
except:
    print("ImportERROR: Cannot find pool.")


class PopUpMat(object):
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.iconbitmap(code_icon)
        self.top.title = "Create Materials CSV"
        self.mat_file = ""
        tk.Button(self.top, text="Select existing Materials file (.csv)", command=lambda: self.select_file()).grid(sticky=tk.EW, row=0, column=0, columnspan=2, pady=yd)
        tk.Label(self.top, text="OR").grid(sticky=tk.EW, row=1, column=0, columnspan=2, padx=xd, pady=yd)
        tk.Button(self.top, text="Open Template", command=lambda: self.open_template()).grid(sticky=tk.EW, row=2, column=0, columnspan=2, pady=yd)
        tk.Button(self.top, fg="RoyalBlue3", bg="white", text="Back", command=lambda: self.cleanup()).grid(sticky=tk.E, row=3, column=1, pady=yd)

    def open_template(self):
        showinfo("INFO", "Do not forget to save this file as a copy before editing.", parent=self.top)
        webbrowser.open(dir2templates + "files/materials.csv")

    def select_file(self):
        showinfo("INFO", "Do not forget to save this file in csv format.", parent=self.top)
        self.mat_file = askopenfilename(initialdir=dir2master, title="Select Materials file",
                                        filetypes=[('Materials', '*.csv;*xls;*xlsm;*xlsx')], parent=self.top)

    def cleanup(self):
        self.top.destroy()
