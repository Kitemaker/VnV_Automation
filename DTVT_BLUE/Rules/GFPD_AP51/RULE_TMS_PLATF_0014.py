### ========= Template =========================================================================
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

### ======== Template Ends===============================================================================================

### =========Rule RULE_TMS_PLATF_0014 ===================================================================================
# Author : Saleem Javed
# Updated 11 April 2017
# Caps Used : Urbalis_Sectors_Cap, Platforms_cap
# Constant used :  None
###======================================================================================================================

# Create Report
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Urbalis Sector", "Platform","Track","Pre_Platform_SSP_ID_LIST" , "Result"])
rwCount = rwCount+1

# Read Caps
urbalis_sectors_cap = SyDT['Urbalis_Sectors_Cap']
urbalis_sector_name = urbalis_sectors_cap['Name']
track_id_list = urbalis_sectors_cap['Track_ID_List']
pre_arrival = urbalis_sectors_cap['Pre_Arrival']

platforms_cap = SyDT['Platforms_Cap']
platform_name = platforms_cap['Name']
plt_track_id = platforms_cap['Track_ID']
pre_platform_ssp_id_list = platforms_cap['Pre_Platform_SSP_ID_List']


for index in range(len(urbalis_sector_name)):
    if (str.upper(pre_arrival[index]) == "TRUE"):
        for pt in range(len(platform_name)):
            if plt_track_id[pt] in track_id_list[index].split(';'):
                if len(pre_platform_ssp_id_list[pt].split(';')) > 0 :
                    result = 'OK'
                    global_test_results.append('OK')
                else:
                    result  = 'NOK'
                    global_test_results.append('NOK')
                    dtvt_log.error("For platform  " + platform_name[pt] +  "Pre_Platform_SSP_ID_List  is not defined " + pre_platform_ssp_id_list[pt])


            Utility.WriteToWorkSheet(wsRpt,rwCount,[urbalis_sector_name[index] ,platform_name[pt], plt_track_id[pt], pre_platform_ssp_id_list[pt] , result ])   
            rwCount = rwCount+1
            
        
# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)