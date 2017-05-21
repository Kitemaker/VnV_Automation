### ========= Template =========================================================================
import sys , os , os.path
import logging
from openpyxl import workbook, worksheet
# add root folder in search path
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(root_folder)
import DtvtLib
from DtvtLib import Utility, Configuration , CSVReader
param = Utility.Initialise(root_folder,__file__)
log_file_path    = param['log_file_path']
result_file_name = param['result_file_name']
result_file_path = param['result_file_path']
dtvt_log         = param['dtvt_log']
proj_const       = param['proj_const']
SyDT             = param['SyDT']

### ======== Template Ends===============================================================================================

### =========Rule RULE_TMS_PLATF_0003 ===================================================================================
# Author : Saleem Javed
# Updated 11 April 2017
# Caps Used : Platforms_cap
# Constant used :  C_Late_Change_Distance
###======================================================================================================================

c_late_change_dist = Utility.Get_C_Late_Change_Distance(param['config'].C_Late_Change_Distance_File_Path)

# Create Report
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Platform", "C_Late_Change_Distance from RTI","C_Late_Change_Distance from SyDT","Result"])
rwCount = rwCount+1

# Read Caps
platforms_cap = SyDT['Platforms_Cap']
platform_name = platforms_cap['Name']
plt_c_late_cng_dist = platforms_cap['C_Late_Change_Distance']


for plt in platform_name:
    res = 'NOK'
    if c_late_change_dist.get(plt) == None :
        dtvt_log.error("For platform "+ plt + "C_Late_Change_Distance not found")
        res = 'NOK'
        global_test_results.append(res)
        global_test_results.append(res)
        Utility.WriteToWorkSheet(wsRpt,rwCount,[plt, "Not Found",plt_c_late_cng_dist[platform_name.index(plt)],res])
        rwCount = rwCount+1

    else:
        if int(c_late_change_dist[plt]) == int(plt_c_late_cng_dist[platform_name.index(plt)]):
            res = 'OK'
            global_test_results.append(res)

        else:
            dtvt_log.error("For platform "+ plt + "C_Late_Change_Distance does not match")
            res = 'NOK'
            global_test_results.append(res)
        Utility.WriteToWorkSheet(wsRpt,rwCount,[plt, c_late_change_dist[plt] , plt_c_late_cng_dist[platform_name.index(plt)] , res])        
        rwCount = rwCount+1

# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)