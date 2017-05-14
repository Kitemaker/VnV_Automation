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

### =========Rule RCD_SIGNAL_0001 ===================================================================
# Author : Saleem Javed
# Updated 11 April 2017
# Caps Used : Signals_Cap  , Service_Stopping_Points_Cap
# Constant used :  None 
###==================================================================================================


csv_reader = CSVReader.CSVReader(config.csv_folder_path)
SyDT = csv_reader.SyDT   

# Read Caps
signals_cap = SyDT[csv_reader.Signals_Cap]
sig_name = signals_cap['Name']
sig_ssp = signals_cap['SSP_ID']
sig_kp = Utility.GetKpValue(signals_cap['KpValue'],signals_cap['KpCorrected_Trolley_Value'])
ssp_cap =  SyDT[csv_reader.Service_Stopping_Points_Cap]
ssp_name = ssp_cap['Name']
ssp_kp = Utility.GetKpValue(ssp_cap['KpValue'],ssp_cap['KpCorrected_Trolley_Value'])

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Signal","Signal_Kp", "SSP","SSP_Kp", "Distance between Signal and SSP","Result"])
rwCount = rwCount+1

for index in range(len(sig_ssp)):
    if sig_ssp[index] != '0':
        try:
            _result='NOK'
            _sig = sig_name[index].strip()
            _sig_kp = sig_kp[index]
            _linked_ssp_name = sig_ssp[index]
            _linked_ssp_index = ssp_name.index(_linked_ssp_name)
            _linked_ssp_kp = ssp_kp[_linked_ssp_index]

            
             # Note: kp values are considered positive , and kps are measured in cms
             # 200 cm is taken from rule definition
            _dist =   abs( _sig_kp - _linked_ssp_kp)
            if _dist >= 200 :
                 tis_log.info('Signal:' + _sig  + ', SSP: '+ _linked_ssp_name + ' ,Distance: ' + str( _dist))
                 _result = 'OK'
                 global_test_results.append(_result)
            else:
                tis_log.error('Signal:' + _sig  + ', SSP: '+ _linked_ssp_name + ' ,Distance: ' + str( _dist))
                _result = 'NOK'
                global_test_results.append(_result)
            
            Utility.WriteToWorkSheet(wsRpt,rwCount,[_sig,_sig_kp,_linked_ssp_name,_linked_ssp_kp,str(_dist),_result])           
            rwCount = rwCount+1

        except:
            tis_log.error( "Module:RCD_SIGNAL_0001.py" + "Method:__main__ " +"item =" + sig_ssp[index]  + "\t" +  sys.exc_info()[0])        

# Save Report

Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
