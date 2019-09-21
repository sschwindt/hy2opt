import os


class ModelControl:
    def __init__(self):
        """
        Variables contain LISTs of possible choices for Tuflow command parameters
        dict DICTIONARIES have keys corresponding to exact names of Tuflow command parameters and values are LISTs of choices
        """

        # MODEL FRAME CONTROL PARAMETERS
        self.hardware = ["CPU", "GPU"]
        self.license_type = ["full", "demo"]
        self.model_precision = ["SINGLE", "DOUBLE"]
        self.solution_scheme = ["HPC", "CLASSIC", "HPC 1st"]
        self.units = ["METRIC", "US Customary", "ENGLISH", "IMPERIAL"]
        self.tcf_dict = {"Hardware": self.hardware,
                         "License": self.license_type,
                         "Model Precision": self.model_precision,
                         "Solution Scheme": self.solution_scheme,
                         "Units": self.units}

        # MODEL STABILITY PARAMETERS
        self.cell_size = [1.]  # [m] Tuflow default
        self.cell_wet_dry = [0.002]  # [m] Tuflow default
        self.dt = [1.0]
        self.iwl = ["AUTO"]
        self.viscosity_s = [0.5]  # [-] Smagorinsky Tuflow defaults
        self.viscosity_c = [0.05]  # [[m2/s] Tuflow defaults
        self.viscosity_f = ["SMAGORINSKY", "CONSTANT"]
        self.sta_dict = {"Cell Size": self.cell_size,
                         "Cell Wet/Dry Depth": self.cell_wet_dry,
                         "Set IWL": self.iwl,
                         "Timestep": self.dt,
                         "Viscosity Formulation": self.viscosity_f,
                         "Smagorinsky Viscosity Coefficient": self.viscosity_s,
                         "Constant Viscosity Coefficient": self.viscosity_c}

        # MODEL OUTPUT PARAMETERS
        self.map_out_format = ["ASC", "DAT", "FLT", "GIS", "GRID", "NC", "T3", "TGO", "TMO", "WRB", "WRC", "WRR", "XMDF"]
        self.map_dat_xmfd_opts = ["SMS", "SMS TRIANGLES", "SMS HIGH RES",
                                  "SMS HIGH RES CORNERS ONLY"]  # if DAT > append SMS automatically - ENABLE MULTIPLE SELECTION!
        self.map_out_intv = [600]  # [s] wrong definition will result in ERROR 0045
        self.map_out_data = ["AP", "BSS", "CI", "Cr", "CWF", "d", "dGW", "E", "F", "FLC", "h", "IR", "MB1", "MB2", "n",
                             "q", "R", "RC", "RFC", "RFML", "RFR", "SP", "SS", "t", "tau", "V", "W", "ZH"]

        """ HAZARD MAPPING PARAMETERS - CURRENTLY UNUSED
        self.map_out_haz = ["Z0", "Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8", "Z9", "ZAEM1", "ZMBRC", "ZMW1",
                            "ZMW2",
                            "ZMW3", "ZPA", "ZPC", "ZPI", "ZQRA", "ZTMR", "ZUK0", "ZUK1", "ZUK2", "ZUK3", "ZUSA1",
                            "ZV"]  # ENABLE MULTIPLE SELECTION!
        """

        self.map_out_dict = {"Map Output Format": self.map_out_format,
                             "Map Output Data Types": self.map_out_data,
                             "Map Output Interval": self.map_out_intv,
                             }


        # RESTART PARAMETERS for optimization
        self.rst_file = [".trf_file"]
        self.rst_dict = {"Read Restart File": self.rst_file}

        self.ctrl_name_dict = {"ctrl": "Model Controls",
                                  "stab": "Stability Parameters",
                                  "out": "Output Parameters",
                                  "rst": "Restart Options (Optimization)"}
        self.ctrl_par_dict = {"ctrl": self.tcf_dict,
                                 "stab": self.sta_dict,
                                 "out": self.map_out_dict,
                                 "rst": self.rst_dict}
        self.ctrl_bg_colors = {"ctrl": "light blue",
                                  "stab": "sky blue",
                                  "out": "steel blue",
                                  "rst": "SeaGreen1"}

    def __call__(self, *args, **kwargs):
        print("Class Info: <type> = ModelControl (%s)" % os.path.dirname(__file__))
        print(dir(self))
