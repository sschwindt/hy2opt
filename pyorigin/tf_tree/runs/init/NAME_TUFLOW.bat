Set TF_SP="D:\Tuflow_2018\TUFLOW_2018-03-AB\TUFLOW_iSP_w64.exe"
Set TF_DP="D:\Tuflow_2018\TUFLOW_2018-03-AB\TUFLOW_iDP_w64.exe"

Set RUN=Start "TUFLOW" /wait %TF_SP%

%RUN%  -b -x -e __user_event__ 	"TUFLOW_OUTPUT_FOLDER\runs\NAME.tcf" 
exit