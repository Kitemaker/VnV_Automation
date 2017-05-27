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

### =========RULE_STOPPING_AREA_0008===============================================================
# Author : Saleem Javed
# Updated 23 May 2017
# Caps Used : Projects_Cap,
# Constant used :  None 

###================================================================================================

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Project Name", "Max_Blocks_With_Work_Zone","Result"])
rwCount = rwCount+1

# Read Caps
project_cap = SyDT['Projects_Cap']
project_names = project_cap['Name']
Max_Blocks_With_Work_Zone = project_cap['Max_Blocks_With_Work_Zone']
_result = ''
for index in range(len(project_names)):
    proj_name = project_names[index]
    max_blocks_with_wz = int(Max_Blocks_With_Work_Zone[index])
    if max_blocks_with_wz <=1000:
        _result = 'OK'
        global_test_results.append('OK')
        dtvt_log.info('Project ' + proj_name  + 'has Blocks_With_Work_Zone less than 1000,  Max_Blocks_With_Work_Zone = ' + str(max_blocks_with_wz))
    else:
        _result = 'NOK'
        global_test_results.append('NOK')
        dtvt_log.error('Project ' + proj_name  + 'has Blocks_With_Work_Zone more than 1000,  Max_Blocks_With_Work_Zone = ' + str(max_blocks_with_wz))


    Utility.WriteToWorkSheet(wsRpt,rwCount,[proj_name,max_blocks_with_wz,_result])
    rwCount = rwCount+1

# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
