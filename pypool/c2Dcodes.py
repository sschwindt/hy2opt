# !/usr/bin/python
try:
    import sys, os, logging
    import subprocess
    from shutil import copytree, copyfile
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys, logging, shutil, subprocess")

try:
    import config as cfg
    import fGlobal as fGl
except:
    print("ExceptionERROR: Cannot access pypool files.")

class CodeMaster:
    def __init__(self, license_type=str(), software_id=str()):
        """
        :param license_type: STR either "full" or "limited"
        :param software_id:  STR listed in cfg.software_ids
        """
        self.logger = logging.getLogger("logfile")
        self.license_type = license_type
        self.model_dir = cfg + software_id + "_models/"
        self.model_name = ""
        self.run_id = "%003i" % 0  # use 3-digit number
        self.software_id = software_id
        self.template = "{0}{1}_tree/".format(cfg.dir2templates, software_id)

    def geo_file_dialogue(self):
        dialogue = fGl.read_file_content(cfg.dir2dialogues + self.software_id + "_geofile_creation.txt")

    def update_model_name(self, model_name):
        self.model_name = model_name
        self.model_dir = cfg.dir2master + model_name + "/"

    def __call__(self):
        print("Class Info: <type> = ModelMaster (%s)" % os.path.dirname(__file__))
        print(dir(self))


class Tuflow(CodeMaster):
    def __init__(self, license_type):
        CodeMaster.__init__(self, license_type, "tf")
        self.sub_folders = ["bc_dbase", "check", "model", "runs", "results"]

    def make_batchfile(self, bat_template, **kwargs):
        """ opens .bat file and rewrites commands
        :param bat_template: STR of full path of the batchfile to be modified
        :param kwargs: run_number: STR of 3-digits run name
        """
        add_run = None
        # parse optional keyword arguments
        for k in kwargs.items():
            if "run_number" in k[0]:
                add_run = str(k[1])

        with open(bat_template, 'r+') as batfile:
            text = batfile.read()
            if "init" in str(bat_template).lower():
                text = text.replace("TUFLOW_OUTPUT_FOLDER", self.model_dir.strip("/").replace("/", "\\"))
                text = text.replace("runs\\NAME", "runs\\init\\" +  self.model_name)
            if add_run:
                if "__user_event__" in text:
                    text = text.replace("__user_event__", add_run)
                else:
                    text = text.split("exit")[0]
                    text = text + '%RUN%  -b -x -e {0} 	\"TUFLOW_OUTPUT_FOLDER\\runs\\NAME.tcf\"\nexit'.format(str(add_run))
            batfile.seek(0)
            batfile.write(text)
            batfile.truncate()

    def make_file_structure(self, model_name):
        self.update_model_name(model_name)
        self.logger.info(" * copying template folder tree (source: %s) ..." % self.template)
        copytree(self.template, self.model_dir)
        self.logger.info(" * renaming model files ...")
        for sub_folder in self.sub_folders:
            if os.path.isdir(self.model_dir + sub_folder + "/init/"):
                src_dir = self.model_dir + sub_folder + "/init/"
            else:
                src_dir = self.model_dir + sub_folder + "/"
            for src_f in fGl.list_file_type_in_dir(src_dir, "*"):
                if "NAME" in str(src_f):
                    prefix, suffix = src_f.split("NAME")
                else:
                    continue
                try:
                    os.rename(src_f, "{0}{1}{2}".format(prefix, model_name, suffix))
                except:
                    self.logger.error("Failed to rename %s. Ensure that no other program uses the file." % str(src_f))
        self.logger.info(" * adapting batchfile template ...")
        self.make_batchfile(self.model_dir + "runs/init/" + self.model_name + "_TUFLOW.bat")

    def make_tbc(self):
        with open(os.path.join(self.model_dir, self.model_name + ".tbc"), 'r+') as myfile:
            text = myfile.read().replace("NAME", self.model_name)
            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()

    def make_tcf(self):
        f = open(os.path.join(self.model_dir + self.run_id, self.model_name + ".tcf"), "a")
        iwl = 0
        cell_depth = 0
        end_time = 0
        timestep = 0
        mapOutput = 0
        mapOutputInterval = 0
        tsOutputInterval = 0
        f.write("\nDemo Model == ON" +
                "\n" +
                # "\nUnits == US Customary" +
                "\nGeometry Control File  ==  ..\\..\\model\\" + self.model_name + ".tgc" +
                "\nBC Control File == ..\\..\\model\\" + self.model_name + ".tbc" +
                "\nBC Database == ..\\..\\bc_dbase\\" + self.run_id + "\\2d_bc_" + self.model_name + ".csv" +
                "\nRead Materials File == ..\\..\\model\\materials.csv" + "     ! This provides the link between the material ID defined in the .tgc and the Manning's roughess" +
                "\nRead GIS PO == ..\\..\\model\\gis\\2d_po_" + self.model_name + "_P.shp" + "     ! velocity monitoring point locations" +
                "\nRead GIS PO == ..\\..\\model\\gis\\2d_po_" + self.model_name + "_L.shp" + "     ! flow monitoring xs lines" +
                "\n" +
                "\nViscosity Formulation == SMAGORINSKY" +
                "\nViscosity Coefficients == 0.5, 0.005" +
                "\nSET IWL == " + iwl + "   ! matches the downstream WSE" +
                "\nCell Wet/Dry Depth == " + cell_depth + "     ! Forces cells to be dry if their depth is < 0.1 m" +
                "\n" +
                "\nStart Time == 0" + "     ! Start Simulation at 0 hours" +
                "\nEnd Time == " + end_time + "     ! End Simulation (hrs)" +
                "\nTimestep == " + timestep + "     ! Use a 2D time step that is ~1/4 of the grid size in m (10 m * 0.25 -> 2.5 s)" +
                "\n" +
                "\nLog Folder == Log" + "   ! Redirects log output (eg. .tlf and _messages GIS layers to the folder log" +
                "\nOutput Folder == ..\\..\\results\\" + self.run_id + "\\" + "     ! Redirects results files to TUFLOW\Results\RUN" +
                "\nWrite Check Files == ..\\..\\check\\" + self.run_id + "\\" + "   ! Specifies check files to be written to TUFLOW\check\RUN" +
                "\nMap Output Format == GRID XMDF" + "  ! Output directly to GIS (grid) as well as SMS (xmdf compact) format" +
                "\nMap Output Data Types == h d n V BSS" + "    ! wse depth Manning's n velocity bed shear stress" +
                "\nStart Map Output == " + mapOutput + "    ! Start map output at 0 hours" +
                "\nMap Output Interval == " + mapOutputInterval + "     ! Output every 600 seconds (10 minutes)" +
                "\nGRID Map Output Data Types == h d n V BSS" +
                "\nTime Series Output Interval  == " + tsOutputInterval + "     ! time interval of output in seconds"
                )

    def make_tef(self):
        print("Go to ArcGIS and edit GIS files in model/gis. When finished in Arc, resume by entering a value for DS water surface elevation...")
        iwl = input("Downstream water surface elevation [m] (e.g. 1003.432) -> ")  # or "1003.432"
        print("Values inside the parenthesis are default values. Hit enter to accept default value or update with new value by typing in value and hitting enter.")
        
        cell_depth = input("Cell Wet/Dry Depth(0.1 m) -> ") or "0.1"
        end_time = input("End Time(2 hrs) -> ") or "2"
        timestep = input("Time Step(2.5 s) NOTE: use timestep that is 1/4 of grid size in meters -> ") or "2.5"
        mapOutput = input("Start Map Output(0 s) -> ") or "0"
        mapOutputInterval = input("Map Output Interval(600 s) -> ") or "600"
        tsOutputInterval = input("Time Series Output Interval(60 s)  -> ") or "60"

        for i in range(int(self.run_id)):
            self.run_id = "00" + str(i + 1)

    def make_tgc(self):
        with open(os.path.join(self.model_dir, self.model_name + ".tgc"), 'r+') as myfile:
            print("If you haven't done so already, use the measure tool in ArcGIS to obtain the x,y dimension (m) of the code area polygon...")

            cell_size = input("Cell Size of code area polygon(10 m)-> ") or "10"
            grid_size = input("Grid Size [m] (x,y dimension of the code area polygon rounded to be divisible by the cell size, e.g. 770,150)-> ")  # or "770,150"
            z_pts = input("Zpts(10000 m) (any elevation notably higher than project max z) -> ") or "10000"

            text = myfile.read().replace("NAME", self.model_name)
            text = text.replace("Cell Size == 10", "Cell Size == " + cell_size)
            text = text.replace("Grid Size (X,Y) == ",  # 770,150",
                                "Grid Size (X,Y) == " + grid_size)
            text = text.replace("Set Zpts == 10000", "Set Zpts == " + z_pts)

            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()

    def prepare_run(self, run_number):
        # run_number = max. 3-digits STR or INT
        run_number = "%003i" % int(run_number)
        if not os.path.isfile(self.model_dir + "runs/" + self.model_name + "_TUFLOW.bat"):
            try:
                copyfile(self.model_dir + "runs/init/" + self.model_name + "_TUFLOW.bat",
                         self.model_dir + "runs/" + self.model_name + "_TUFLOW.bat")
            except:
                self.logger.error("Failed to copy {0} to {1}. Ensure that {0} exists and that {1} is not opened in any program.".format(self.model_dir + "runs/init/" + self.model_name + "_TUFLOW.bat", self.model_dir + "runs/" + self.model_name + "_TUFLOW.bat"))
        self.make_batchfile(self.model_dir + "runs/" + self.model_name + "_TUFLOW.bat", run_number=run_number)
        copyfile(self.model_dir + "bc_dbase/init/2d_bc_" + self.model_name + ".csv",
                 self.model_dir + "bc_dbase/2d_bc_" + self.model_name + "_" + run_number + ".csv")
        copyfile(self.model_dir + "runs/init/" + self.model_name + ".tcf",
                 self.model_dir + "runs/" + self.model_name + "_" + run_number + ".tcf")
        copyfile(self.model_dir + "runs/init/" + self.model_name + ".tef",
                 self.model_dir + "runs/" + self.model_name + "_" + run_number + ".tef")


    def prepare_geofiles(self, src_projection):
        # src_projection = STR of source .prj file path, e.g. "output_folder/shp_files/" + NAME + "_bound_rec.prj"
        copyfile(src_projection, self.model_dir + "/model/gis/projection.prj")

        desired_files = ["2d_code_empty_R", "2d_loc_empty_L",
                         "2d_mat_empty_R", "2d_po_empty_L", "2d_po_empty_P"]

        for f in os.listdir(self.model_dir + "/gis/empty"):
            file_path = os.path.join(self.model_dir + "/gis/empty", f)

            if f.split(".")[0] == '2d_sa_empty_R':
                des_path = os.path.join(
                    self.model_dir + "/gis", f.replace("_empty_", "_" + self.model_name + "_QT_"))
            elif f.split(".")[0] == '2d_bc_empty_L':
                des_path = os.path.join(
                    self.model_dir + "/gis", f.replace("_empty_", "_" + self.model_name + "_HT_"))
            elif f.split(".")[0] in desired_files:
                des_path = os.path.join(
                    self.model_dir + "/gis", f.replace("_empty_", "_" + self.model_name + "_"))
            else:
                continue
            copyfile(file_path, des_path)
    
    def run(self, batchfile_dir):
        # batchfile_dir = STR of full dir and name of the batchfile for running Tuflow
        p = subprocess.Popen(batchfile_dir, shell=True, stdout=subprocess.PIPE)
        print("\nAfter empty template GIS files are created, hit Enter to continue...\n")
        p.communicate()

    def __call__(self):
        print("Class Info: <type> = Tuflow (%s)" % os.path.dirname(__file__))
        print(dir(self))
