try:
    import os, sys
except:
    print("ERROR: Could not import basic packages (os, sys).")

try:
    import config as cfg
    import c2Dcodes as c2D
    import fGlobal as fGl
except:
    print("ERROR: Could not import pypool scripts.")

def main(software_name, license_type, model_name):
    """
    software_name = STR of 2D modelling software (e.g., "Tuflow")
    license_type = STR, either "full" or "limited"
    model_name = STR of model (e.g., "A_Unique_Reach_2008")
    """
    if "tuflow" in software_name.lower():
        model = c2D.Tuflow(license_type)
    else:
        return print("No valid model name found (provided %s)." % str(software_name))
    
    if not fGl.chk_dir(model.model_dir + model_name):
        model.make_file_structure(model_name)
        model.file_dialogue()
    else:
        model.update_model_name(model_name)
        
    
    
    
    


if __name__ == '__main__':
    software_name = "Tuflow"
    license_type = "full"
    model_name = "testbed_river"
    main(software_name, license_type, model_name)



from copyfiles import copyfiles
from copyfiles import parameters
from update_attri_table import update_attri_table
from run_tuflow import run_tuflow
#from run_tuflow import bc_data
from arcpy import env
from bankfull_stage_flow import stage_flow_inputs
from float2raster import flt_to_tif
from distutils.dir_util import copy_tree
 
import numpy as np
os.chdir("C:/Git_hub/tuflow-wf_python3")
env.workspace = "C:/Git_hub/tuflow-wf_python3"

area = 638 # km2
wCV = 0.08
dCV = 0.29
    
dCoVar = 1    # 1: shallow, -1: deep, 0 median 
wCoVar =  1   # -1: narrow,1 wide 0 median 
wd_ratio = 26.49
width_m = 3.45*area**0.39
    
# arbitrary datum for the top of bank
z_bf = 10
n = 0.035  # Manning's n 
S = 0.0012 # slope

# the stage (fraction of bankfull) to be evaluated 
stages = np.array([0.01,0.02,0.05,0.08,0.1,0.12,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.8,1])
depth_bf, df = stage_flow_inputs(stages,area,wCV,dCV,dCoVar,wCoVar,wd_ratio,width_m,z_bf,n,S)

Elevation = 984.5  # the bottom elevation (m)
NAME = 'SFE95'  # file name of the ascii file
meter = '-2'  #buffer by x meters
run_number = str(len(stages))  # how many discharge you want to run
create_boundary(NAME, meter)
generate_file_structure(NAME,run_number)

copyfiles(NAME,run_number)

#
cell_size = "2"
#cell_size = "2"
grid_size = "500,700"
# copy GIS files to "\output_folder\sfe5_tuflow\Model

parameters(NAME, run_number, cell_size, grid_size)
#update_attri_table(NAME)   # just copy the files in which the attributes are updated
# skip update_attri_table if you are using the updated files

run_tuflow(NAME, run_number)  #the results are stored in /results/grid/*.flt (raster files)
# bc_data.csv need to be placed in the input folder
flt_to_tif(NAME, run_number)  #convert .flt files to .tif files
