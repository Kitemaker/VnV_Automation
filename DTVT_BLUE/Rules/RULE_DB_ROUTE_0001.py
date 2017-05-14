### ========= Template =========================================================================
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

### ======== Template Ends===========================================================================

### =========Rule RULE_DB_ROUTE_0001 ===================================================================
# Author : Saleem Javed
# Updated 4 May 2017
# Caps Used : Signals_Cap,Routes_Cap,Signalisation_Areas_Cap
# Constant used :  None 
###==================================================================================================


csv_reader = CSVReader.CSVReader(config.csv_folder_path)
SyDT = csv_reader.SyDT   

# Read Caps
routes_cap = SyDT[csv_reader.Routes_Cap]
signals_cap = SyDT[csv_reader.Signals_Cap]
sig_area_cap = SyDT[csv_reader.Signalisation_Areas_Cap]

route_name = routes_cap['Name']
route_orig_signal = routes_cap['Origin_Signal_ID']

sig_name = signals_cap['Name']
sig_sdd = signals_cap['Secondary_Detection_Device_ID']

sig_area_name = sig_area_cap['Name']
sig_area_type = sig_area_cap['Area_Type']
sig_area_sdd = sig_area_cap['Area_Boundary_Secondary_Detection_Device_ID_List']


# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Route", "Origin_Signal", "SDD", "Signalisation Area", "Result"])
rwCount = rwCount+1

for index in range(len(route_name)):
    try:
        _result = ""
        _route = route_name[index]
        _orig_sig = route_orig_signal[index]
        _sdd = sig_sdd[sig_name.index(_orig_sig)]
        _sdd_sig_area = ""    
        if _sdd != '0':
            for item in range(len(sig_area_name)):                
                if sig_area_type[item] =="CBI":
                    _sig_area = sig_area_name[item]
                    if _sdd in sig_area_sdd[item].split(';'):
                        _sdd_sig_area = _sig_area
                        _result = 'OK'
                        global_test_results.append(_result)
                        tis_log.info('SDD of Route:' + _route  + ', Protected by Orgin Signal '+_orig_sig + ' belongs to  CBI Signalosation area:' + _sdd_sig_area)
                        break
            if _sdd_sig_area == "":
                _result = 'NOK'
                global_test_results.append(_result)
                tis_log.error('SDD of Route:' + _route  + ', Protected by Orgin Signal '+_orig_sig + ' Does not belog to any CBI Signalosation area')
        else:
            _sdd = ""
            _sdd_sig_area = ""
            _result = "OK"

        Utility.WriteToWorkSheet(wsRpt,rwCount,[_route,_orig_sig,_sdd,_sdd_sig_area,_result])    
        rwCount = rwCount+1

    except:
        tis_log.error( "Module:RULE_DB_ROUTE_0001.py" + "Method:__main__ " +"item =" + route_name + "\t" +  sys.exc_info()[0])        

# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
