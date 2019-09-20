from cCtrl import ModelControl
from cGeo import ModelGeoControl
from cBCevents import ModelEvents
from config import *
import fileinput


class Hy2OptModel(ModelControl, ModelGeoControl, ModelEvents):
    # name = ReadOnlyParameter("model_name")
    # model_file = ReadOnlyParameter(dir2tf + "models/model_name.hy2model")

    def __init__(self, model_name):
        self._name = model_name
        self._model_file = dir2tf + "models/" + model_name + ".hy2model"

        ModelControl.__init__(self)
        ModelGeoControl.__init__(self)
        ModelEvents.__init__(self)

        # Control par_group dicts
        self.tcf_applied_dict = {}
        self.sta_applied_dict = {}
        self.out_applied_dict = {}
        # Geo par_group dicts
        self.tgc_applied_dict = {}
        self.mat_applied_dict = {}
        self.tbc_applied_dict = {}
        # BC par_group dicts
        self.bce_applied_dict = {}
        self.bat_applied_dict = {}

        self.par_dict = {"ctrl": self.tcf_applied_dict, "stab": self.sta_applied_dict, "out": self.out_applied_dict,
                         "gctrl": self.tgc_applied_dict, "gmat": self.mat_applied_dict, "gbc": self.tbc_applied_dict,
                         "bce": self.bce_applied_dict, "bat": self.bat_applied_dict}

        self.complete()

    def complete(self):
        for k in self.tcf_dict.keys():
            self.tcf_applied_dict.update({k: ""})
        for k in self.sta_dict.keys():
            self.sta_applied_dict.update({k: ""})
        for k in self.map_out_dict.keys():
            self.out_applied_dict.update({k: ""})
        for k in self.geo_tgc_dict.keys():
            self.tgc_applied_dict.update({k: ""})
        for k in self.geo_mat_dict.keys():
            self.mat_applied_dict.update({k: ""})
        for k in self.geo_tbc_dict.keys():
            self.tbc_applied_dict.update({k: ""})
        for k in self.event_dict.keys():
            self.bce_applied_dict.update({k: ""})
        for k in self.bat_dict.keys():
            self.bat_applied_dict.update({k: ""})

    @property
    def model_file(self):
        return self._model_file

    @model_file.setter
    def model_file(self, val):
        raise Exception("Read-only: Use Hy2OpModel.set_parameter_... instead.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        raise Exception("Read-only: Use Hy2OpModel.set_parameter_... instead.")

    def read_model(self):
        pass

    def replace_model_par(self, search_pattern, new_line_str):
        """
        Replace lines that start with a pattern
        :param search_pattern: STR
        :param new_line_str: STR
        """
        for line in fileinput.input([self.model_file], inplace=True):
            if line.strip().startswith(search_pattern):
                line = new_line_str
            sys.stdout.write(line)

    def save_model(self):
        for k, v in self.par_dict.items():
            for e in v.keys():
                self.write_parameter(k, e)

    def set_model_name(self, model_name):
        self._name = model_name
        self._model_file = dir2tf + "models/" + model_name + ".hy2model"

    def set_usr_parameters(self, par_group, par, values):
        """
        Writes user values in par_dict
        :param par_group: STR corresponding to self.par_dict.keys()
        :param par: STR corresponding to self.par_dict.keys()
        :param values: LIST with one or more values to be written in one line of a (TCF/TGC/TBC/TEF) file
        :return: None
        """
        if values.__len__() > 1:
            val_str = " ".join(values)
        else:
            val_str = str(values[0])
        self.par_dict[par_group][par] = val_str
        self.write_parameter(par_group, par)

    def write_parameter(self, par_group, par):
        write_str = "{0}::{1}::".format(par_group, par)
        if os.path.isfile(self.model_file):
            if write_str in open(self.model_file).read():
                self.replace_model_par(write_str, write_str + self.par_dict[par_group][par] + "\n")
                return 0
            f_model = open(self.model_file, "a+")
        else:
            f_model = open(self.model_file, "w")
        # f_model.seek(0)
        f_model.write(write_str + self.par_dict[par_group][par] + "\n")
        f_model.truncate()

    def __call__(self, *args, **kwargs):
        print("Class Info: <type> = Hy2OptModel (Tuflow) (%s)" % os.path.dirname(__file__))
        print(dir(self))
