### ========= Template =====================================================================================================
import sys
import os,os.path
import logging
from openpyxl import workbook, worksheet

# add root folder in search path
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(root_folder)

import TisLib
from TisLib import Utility, Configuration , CSVReader

try:
    # Get Tis_Logger and specify the log file name   
    log_file_path = os.path.join(root_folder + "\\Logs\\" , os.path.basename(__file__).split('.')[0] + '.log')
    result_file_name = os.path.basename(__file__).split('.')[0] + '.xlsx'
    result_file_path = os.path.join(root_folder + "\\Results\\" ,'Test_Results_' + result_file_name)
    tis_log = Utility.GetLogger(log_file_path)
except:
    print("Error while creating logger")

config = Configuration.Configuration(root_folder)
# read constant
proj_const = dict()
proj_const = Utility.GetProjectConstants(config.config_File_Path)
print("Executing " + os.path.basename(__file__))
tis_log.info("Executing " + os.path.basename(__file__))

### ======== Template Ends===============================================================================================

### =========Rule RULE_TMS_PLATF_0003 ===================================================================================
# Author : Saleem Javed
# Updated 11 April 2017
# Caps Used : Platforms_cap
# Constant used :  C_Late_Change_Distance
###======================================================================================================================


csv_reader = CSVReader.CSVReader(config.csv_folder_path)
SyDT = csv_reader.SyDT   
c_late_change_dist = Utility.Get_C_Late_Change_Distance(config.C_Late_Change_Distance_File_Path)

# Create Report
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
wsRpt.cell(row = rwCount, column = 1, value = "Platform")
wsRpt.cell(row = rwCount, column = 2, value = "C_Late_Change_Distance from RTI")
wsRpt.cell(row = rwCount, column = 3, value = "C_Late_Change_Distance from SyDT")
wsRpt.cell(row = rwCount, column = 4, value = "Result")
rwCount = rwCount+1

# Read Caps
platforms_cap = SyDT[csv_reader.Platforms_Cap]
platform_name = platforms_cap['Name']
plt_c_late_cng_dist = platforms_cap['C_Late_Change_Distance']



for plt in platform_name:
    res = 'NOK'
    if c_late_change_dist.get(plt) == None :
        tis_log.error("For platform "+ plt + "C_Late_Change_Distance not found")
        res = 'NOK'
        global_test_results.append(res)
        global_test_results.append(res)
        wsRpt.cell(row = rwCount, column = 1, value = plt)
        wsRpt.cell(row = rwCount, column = 2, value = "Not Found")
        wsRpt.cell(row = rwCount, column = 3, value = plt_c_late_cng_dist[platform_name.index(plt)])
        wsRpt.cell(row = rwCount, column = 4, value = res)
        rwCount = rwCount+1

    else:
        if int(c_late_change_dist[plt]) == int(plt_c_late_cng_dist[platform_name.index(plt)]):
            res = 'OK'
            global_test_results.append(res)

        else:
            tis_log.error("For platform "+ plt + "C_Late_Change_Distance does not match")
            res = 'NOK'
            global_test_results.append(res)

        wsRpt.cell(row = rwCount, column = 1, value = plt)
        wsRpt.cell(row = rwCount, column = 2, value =  c_late_change_dist[plt])
        wsRpt.cell(row = rwCount, column = 3, value = plt_c_late_cng_dist[platform_name.index(plt)])
        wsRpt.cell(row = rwCount, column = 4, value = res)
        rwCount = rwCount+1


# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)