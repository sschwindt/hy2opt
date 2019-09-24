import os


class ModelEvents:
    def __init__(self):
        """
        Variables contain LISTs of possible choices for Tuflow command parameters
        dict DICTIONARIES have keys corresponding to exact names of Tuflow command parameters and values are LISTs of choices
        """

        self.bce_rst_dict = {}

        # TEF file contents
        self.bc_list = []  # will be read from 2d_sa_MODEL_QT_R.shp
        self.events = [""]
        self.event_dict = {"Flow1": self.events}
        self.event_desc = {"Flow1": "Steady XXX CMS discharge"}

        # BAT file contents
        # self.bat_opts = []
        # self.bat_dict = {"Batchfiles": self.bat_opts}

        self.bce_name_dict = {"bce": "BC Events",
                              "bat": "Batchfile",
                              "rst": "Restart Options (Optimization)"}

        self.bce_bg_colors = {"bce": "light blue",
                              "bat": "sky blue",
                              "rst": "SeaGreen1"}

    def __call__(self, *args, **kwargs):
        print("Class Info: <type> = ModelEvents (%s)" % os.path.dirname(__file__))
        print(dir(self))
