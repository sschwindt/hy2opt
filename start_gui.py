try:
    import sys, os
    sys.path.append(os.path.dirname(__file__) + "\\pypool\\")
    from config import *
    set_directories()
except:
    print("ERROR: Could not import pypool.")

try:
    import ctypes  # may be required to eget_model_parnable showing the code_icon in taskbar
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass


class ParentGUI(tk.Frame):
    # parent GUI for all modules
    @log_actions
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        self.master.title("H2Opt")
        self.master.iconbitmap(code_icon)

        self.tab_container = ttk.Notebook(master)

        self.tab_names = ['Welcome', 'Tuflow', 'Other']

        self.sub_tab_parents = ['Tuflow',
                                'Other']

        self.sub_tab_names = [['Set Model', 'Run'],
                              ['Set Model', 'Run']]

        # working directory suffixes for each module
        self.tab_dir_names = ['\\pyhi\\',
                              ['\\tuflow\\', '\\tuflow\\'],
                              ['\\other\\', '\\other\\']]

        # Frames initialized by module, with parent being tab container
        self.tab_list = [pyhi.welcome_gui.WelcomeTab(self.tab_container),
                         ttk.Notebook(self.tab_container),
                         ttk.Notebook(self.tab_container)]

        self.tab_dirs = dict(zip(self.tab_names, self.tab_dir_names))
        self.tabs = dict(zip(self.tab_names, self.tab_list))
        self.title = "H2Opt"

        # sub tabs initialized, with parents being associated top-level tabs
        self.sub_tab_list = [[tuflow.tf_gui.TuflowTab(self.tabs['Tuflow']),
                              tuflow.tf_gui.TuflowTab(self.tabs['Tuflow'])],
                             [other.ot_gui.OtherTab(self.tabs['Other']),
                              other.ot_gui.OtherTab(self.tabs['Other'])]]

        self.sub_tab_names = dict(zip(self.sub_tab_parents, self.sub_tab_names))
        self.sub_tabs = dict(zip(self.sub_tab_parents, self.sub_tab_list))

        for tab_name in self.tab_names:
            tab = self.tabs[tab_name]
            tab.bind('<Visibility>', self.tab_select)
            self.tab_container.add(tab, text=tab_name)
            self.tab_container.pack(expand=1, fill="both")
            # set sub-tabs
            if tab_name in self.sub_tab_parents:
                for i, sub_tab_name in enumerate(self.sub_tab_names[tab_name]):
                    sub_tab = self.sub_tabs[tab_name][i]
                    sub_tab.bind('<Visibility>', self.tab_select)
                    tab.add(sub_tab, text=sub_tab_name)

    def tab_select(self, event):
        selected_tab_name = self.tab_container.tab(self.tab_container.select(), 'text')
        if selected_tab_name in self.sub_tab_parents:
            parent = self.tabs[selected_tab_name]
            # names of sub-tabs for this parent
            sub_tab_names = self.sub_tab_names[selected_tab_name]
            # name of selected sub-tab
            selected_subtab_name = parent.tab(parent.select(), 'text')
            # index of sub-tab under parent tab
            i = sub_tab_names.index(selected_subtab_name)
            selected_tab = self.sub_tabs[selected_tab_name][i]
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + self.tab_dirs[selected_tab_name][i])
        else:
            selected_tab = self.tabs[selected_tab_name]
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + self.tab_dirs[selected_tab_name])
        selected_tab.set_geometry(selected_tab.title)
        selected_tab.make_standard_menus()
        # selected_tab.complete_menus()


if __name__ == '__main__':
    ParentGUI().mainloop()
