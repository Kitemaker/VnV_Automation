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

### ======== Template Ends===========================================================================

### =========Rule RCD_TMS_RMZ_016 ===================================================================
# Author : Saleem Javed
# Updated 12 April 2017
# Caps Used : Reverse_Movement_Zones_Cap  , SDDB_Cap
# Constant used :  None
###==================================================================================================

# Read Caps
Dir_In_Increasing_Kp =  str.upper(SyDT['Lines_Cap']['Conventional_Description_Direction'][0])
rmz_cap = SyDT['Reverse_Movement_Zones_Cap']
sddb_cap = SyDT['SDDB_Cap']
trfc_cap = SyDT['TRFC_Cap']

rmz_id = rmz_cap['ID']
rmz_names = rmz_cap['Name']
rmz_track = rmz_cap['Track_ID']
rmz_dir = rmz_cap['Reverse_Movement_Direction']
rmz_type = rmz_cap['RMZ_Type']
rmz_kp_begin = Utility.GetKpValue(rmz_cap['Kp_BeginValue'],rmz_cap['Kp_BeginCorrected_Trolley_Value'])
rmz_kp_end =   Utility.GetKpValue(rmz_cap['Kp_EndValue'],rmz_cap['Kp_EndCorrected_Trolley_Value'])
rmz_trfc_list = rmz_cap['Train_Formation_Characteristics_ID_List']

sddb_name = sddb_cap['Name']
sddb_track  = sddb_cap['Track_ID']
sddb_kp = Utility.SDDBKp(sddb_cap)

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1

Utility.WriteToWorkSheet(wsRpt,rwCount,["RMZ", "RMZ_Type","Track","Kp_Begin_Value","Kp_End_Value","SDDB","SDDB_Track","SDDB_Kp","Result"])
rwCount = rwCount+1

for index in range(len(rmz_names)):
    try:
      
        _rmz = rmz_names[index].strip()
        _rmz_kp_b = int(rmz_kp_begin[index])
        _rmz_kp_e = int(rmz_kp_end[index])
        _rmz_type = rmz_type[index]
        _rmz_track = rmz_track[index]
        _rmz_dir = str.upper(rmz_dir[index])
        if str.upper(rmz_type[index]) == 'RMR_PER_ZONES':

            for sdditem  in range(len(sddb_name)):
                if(sddb_track[sdditem] == _rmz_track):
                    _result=''
                    temp = list([int(sddb_kp[sdditem]),_rmz_kp_b , _rmz_kp_e ])
                    temp.sort()
                    if temp.index(int(sddb_kp[sdditem])) == 1:
                        _result = 'NOK'
                        global_test_results.append('NOK')
                        dtvt_log.error('RMZ:' + _rmz + ', Track: '+ _rmz_track + 'has SDDB ' + sddb_name[sdditem] + "within its boundaries")
                    else:
                        _result = 'OK'
                        global_test_results.append('OK')
                        dtvt_log.info('RMZ:' + _rmz + ', Track: '+ _rmz_track + 'has SDDB ' + sddb_name[sdditem] + "out of its boundaries")

                    Utility.WriteToWorkSheet(wsRpt,rwCount,[_rmz, _rmz_type ,_rmz_track ,_rmz_kp_b,_rmz_kp_e, sddb_name[sdditem] ,sddb_track[sdditem] ,int(sddb_kp[sdditem]),_result])
                    rwCount = rwCount+1

        elif str.upper(rmz_type[index]) == 'REVERSE_JOG':
            form_list =list()
            for tr in rmz_trfc_list[index].split(';'):
                form_list.append( int(trfc_cap['Formation_Length'][trfc_cap['Name'].index(tr)]))

            max_form_length = max(form_list)
            if  _rmz_dir == "BOTH":
                k1 = _rmz_kp_b - max_form_length
                k2 = _rmz_kp_e + max_form_length
            elif _rmz_dir == "UP":
                k1 = _rmz_kp_b - max_form_length
                k2 = _rmz_kp_e
            elif _rmz_dir == "DOWN":
                k1 = _rmz_kp_b 
                k2 = _rmz_kp_e + max_form_length

                for sdditem in range(len(sddb_name)):
                    _result=''
                    temp = list(int(sddb_kp[sdditem]),k1 , k2 )
                    temp.sort()
                    if temp.index(int(sddb_kp[sdditem])) == 1:
                        _result = 'NOK'
                        global_test_results.append('NOK')
                        dtvt_log.error('RMZ:' + _rmz + ', Track: '+ _rmz_track + 'has SDDB ' + sddb_name[sdditem] + "within its boundaries")
                    else:
                        _result = 'OK'
                        global_test_results.append('OK')
                        dtvt_log.info('RMZ:' + _rmz + ', Track: '+ _rmz_track + 'has SDDB ' + sddb_name[sdditem] + "out of its boundaries")

                    Utility.WriteToWorkSheet(wsRpt,rwCount,[_rmz, _rmz_type ,_rmz_track ,_rmz_kp_b,_rmz_kp_e, sddb_name[sdditem] ,sddb_track[sdditem] ,int(sddb_kp[sdditem]),_result])
                    rwCount = rwCount+1
    except:
        dtvt_log.error("Unexpected error, Module Name: RCD_TMS_RMZ_016.py Mthode: Main" , sys.exc_info()[0])



# Save Report

print('Rule Execution Finished. Saveing Report...')
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)


