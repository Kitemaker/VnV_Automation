### ========= Template ============================================================================
import sys , os , os.path
import logging
from openpyxl import workbook, worksheet
# add root folder in search path
root_folder = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),".."))
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

### ======== Template Ends=========================================================================

### =========Rule_WZ_0009===============================================================
# Author : Saleem Javed
# Updated 31 May 2017
# Caps Used : Project_Specific_Boundarys_Cap,
# Constant used :  None 

###================================================================================================

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Boundary Name", "Boundary Type", "Direction"])
rwCount = rwCount+1

# Read Caps
boundary_cap = SyDT['Project_Specific_Boundarys_Cap']
boundary_names = boundary_cap['Name']
boundary_type = boundary_cap['Type']
boundary_dir = boundary_cap['Direction']
_result = ''
for index in range(len(boundary_names)):
    bnd_name = boundary_names[index]
    bnd_type = boundary_type[index]
    bnd_dir = boundary_dir[index]
    if bnd_type !="Dynamic Work Zone" and bnd_dir =="Both":
        _result = 'OK'
        global_test_results.append('OK')
        dtvt_log.info('Project Specific Boundary ' + bnd_name  + 'of type = ' + bnd_type + '  has direction = ' + bnd_dir)
    else:
        _result = 'NOK'
        global_test_results.append('NOK')
        dtvt_log.error('Project Specific Boundary ' + bnd_name  + 'of type = ' + bnd_type + '  has direction = ' + bnd_dir)

    Utility.WriteToWorkSheet(wsRpt,rwCount,[bnd_name,bnd_type,bnd_dir,_result])
    rwCount = rwCount+1

# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
