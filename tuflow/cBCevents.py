import os


class ModelEvents:
    def __init__(self):
        """
        Variables contain LISTs of possible choices for Tuflow command parameters
        dict DICTIONARIES have keys corresponding to exact names of Tuflow command parameters and values are LISTs of choices
        """

        self.bce_rst_dict = {}

        # TEF file contents
        self.events = []
        self.event_dict = {"Flow1": self.events}
        self.event_desc = {"Flow1": "2d_loc_MODEL_L.shp"}

        # BAT file contents
        self.bat_opts = []
        self.bat_dict = {"Batchfiles": self.bat_opts}

        self.section_name_dict = {"bce": "Events",
                                  "bat": "Batchfile",
                                  "rst": "Restart Options (Optimization)"}
        self.section_par_dict = {"bce": self.event_dict,
                                 "bat": self.bat_dict,
                                 "rst": self.bce_rst_dict}
        self.section_bg_colors = {"bce": "light blue",
                                  "bat": "sky blue",
                                  "rst": "SeaGreen1"}

    def __call__(self, *args, **kwargs):
        print("Class Info: <type> = ModelEvents (%s)" % os.path.dirname(__file__))
        print(dir(self))
