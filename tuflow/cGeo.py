import os


class ModelGeoControl:
    def __init__(self):
        """
        Variables contain LISTs of possible choices for Tuflow command parameters
        dict DICTIONARIES have keys corresponding to exact names of Tuflow command parameters and values are LISTs of choices
        """

        # Geodata used with model restart
        self.iwl_grid = ["gis_raster"]  # gis_layer must have .flt or .asc format
        self.geo_rst_dict = {"Read Grid IWL": self.iwl_grid}

        # TGC file contents
        self.shp2d_loc = ["."]
        self.grid_sz = [(0, 0)]
        self.set_z = [3000]
        self.grid_z = ["."]
        self.set_code = [0]
        self.shp2d_code = ["."]
        self.geo_tgc_dict = {"Read GIS Location": self.shp2d_loc,
                             "Grid Size": self.grid_sz,
                             "Set Zpts": self.set_z,
                             "Read GRID Zpts": self.grid_z,
                             "Set Code": self.set_code,
                             "Read GIS Code": self.shp2d_code}

        # MATERIALS as written to TGC
        self.set_mat = [1]
        self.csv_mat = [None]
        self.shp2d_mat = ["."]
        self.geo_mat_dict = {"Set Mat": self.set_mat,
                             "Read Materials File": self.csv_mat,
                             "Read GIS Mat": self.shp2d_mat}



        # TBC file contents
        self.shp2d_bc = ["."]
        self.shp2d_sa = ["."]
        self.geo_tbc_dict = {"Read GIS BC": self.shp2d_bc,
                             "Read GIS SA": self.shp2d_sa}

        self.geo_format_desc = {"Read GIS Location": "2d_loc_MODEL_L.shp",
                                "Grid Size": "X, Y (m or ft)",
                                "Set Zpts": "Int (m or ft)",
                                "Read GRID Zpts": "DEM raster (.asc or .flt)",
                                "Set Code": "Int (0=False, 1=True)",
                                "Read GIS Code": "2d_code_MODEL_R.shp",
                                "Set Mat": "Int (default material ID)",
                                "Read GIS Mat": "2d_mat_MODEL_R.shp",
                                "Read Materials File": "csv file (optional)",
                                "Read GIS BC": "2d_bc_MODEL_HT_L.shp",
                                "Read GIS SA": "2d_sa_MODEL_QT_R.shp"}
        self.section_name_dict = {"gctrl": "Geometry Controls",
                                  "gmat": "Materials",
                                  "gbc": "Geometry Boundaries",
                                  "rst": "Restart Options (Optimization)"}
        self.section_par_dict = {"gctrl": self.geo_tgc_dict,
                                 "gmat": self.geo_mat_dict,
                                 "gbc": self.geo_tbc_dict,
                                 "rst": self.geo_rst_dict}
        self.section_bg_colors = {"gctrl": "light blue",
                                  "gmat": "sky blue",
                                  "gbc": "steel blue",
                                  "rst": "SeaGreen1"}

    def __call__(self, *args, **kwargs):
        print("Class Info: <type> = ModelGeoControl (%s)" % os.path.dirname(__file__))
        print(dir(self))
