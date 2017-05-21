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

### =========Rule RULE_TMS_STABL_0003 ===================================================================
# Author : Saleem Javed
# Updated 12 April 2017
# Caps Used : Tracks_Cap, Stablings_Location_Cap  , TRFC_Cap , Service_Stopping_Points_Cap
# Constant used :  None
###==================================================================================================

# Read Caps
Dir_In_Increasing_Kp =  str.upper(SyDT['Lines_Cap']['Conventional_Description_Direction'][0])

stl_cap = SyDT['Stablings_Location_Cap']
ssp_cap = SyDT['Service_Stopping_Points_Cap']
trfc_cap = SyDT['TRFC_Cap']

stl_id = stl_cap['ID']
stl_names = stl_cap['Name']
stl_track = stl_cap['Track_ID']
# get all occurance of tracks
stl_track_set = set(stl_track)
stl_kp_begin = Utility.GetKpValue(stl_cap['Kp_BeginValue'],stl_cap['Kp_BeginCorrected_Trolley_Value'])
stl_kp_end = Utility.GetKpValue(stl_cap['Kp_EndValue'],stl_cap['Kp_EndCorrected_Trolley_Value'])
stl_ssp_list = stl_cap['SSP_ID_List']

ssp_name = ssp_cap['Name']
ssp_track  = ssp_cap['Track_ID']
ssp_trfc = ssp_cap['Train_Formation_Characteristics_ID_List']
ssp_dir = ssp_cap['Direction']
ssp_kp = Utility.GetKpValue(ssp_cap['KpValue'],ssp_cap['KpCorrected_Trolley_Value'])

trfc_name = trfc_cap['Name']
trfc_form_length = trfc_cap['Formation_Length']

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Stabling", "Track","Kp_Begin","Kp_End","SSP","Direction","Stabling_Length","Train","Train_Length", "Result"])
rwCount = rwCount+1

stl_stl_next = dict()
stl_stl_prev = dict()
for i in range(len(stl_id)):
    for j in range(len(stl_id)):
        if stl_track[i] == stl_track[j]:
            if int(stl_kp_end[i]) == int(stl_kp_begin[j]):
                stl_stl_next[i] = j
                stl_stl_prev[j] = i
                break
        

def GetEndofStablingIncreasing(StablingIndex:int):
    if stl_stl_next.get(StablingIndex) != None:
        return GetEndofStablingIncreasing(stl_stl_next[StablingIndex])
    else:
        return stl_kp_end[StablingIndex]

def GetEndofStablingDecreasing(StablingIndex:int):
    if stl_stl_prev.get(StablingIndex) != None:
        return GetEndofStablingDecreasing(stl_stl_prev[StablingIndex])
    else:
        return stl_kp_begin[StablingIndex]


for index in range(len(stl_names)):
    _stl_name = stl_names[index]
    _track =    stl_track[index]
    if(stl_ssp_list[index] != "0"):
        for _ssp in str.split(stl_ssp_list[index],';'):
            _result = ''
            _ssp_kp = int(ssp_kp[ssp_name.index(_ssp)])
            _dir = ssp_dir[ssp_name.index(_ssp)].upper()
            if _dir == "DOWN":
                _ssp_end_point  =  GetEndofStablingIncreasing(index)
            
            elif _dir == "UP":
                _ssp_end_point  =  GetEndofStablingDecreasing(index)
            
            stabling_length = abs(_ssp_end_point - _ssp_kp)

            for train in str.split(ssp_trfc[ssp_name.index(_ssp)],';'):
                tr_length = int(trfc_form_length[trfc_name.index(train)])
                if(tr_length <= stabling_length):
                    _result = "OK"
                    global_test_results.append('OK')
                    dtvt_log.info('stl_name: ' + _stl_name + ', ssp: '+ _ssp + '  stabling_length   ' + str(stabling_length) + "  Train: "+ train + "  Train Length: " + str(tr_length))
                if(tr_length > stabling_length):
                    _result = "NOK"
                    global_test_results.append('NOK')
                    dtvt_log.error('stl_name: ' + _stl_name + ', ssp: '+ _ssp + '  stabling_length  ' + str(stabling_length) + "  Train: "+ train + "  Train Length: " + str(tr_length))

            Utility.WriteToWorkSheet(wsRpt,rwCount,[_stl_name, _track ,stl_kp_begin[index],stl_kp_end[index],_ssp ,_dir,stabling_length,train , str(stabling_length) , str(tr_length)])
            rwCount = rwCount+1


# Save Report

print('Rule Execution Finished. Saveing Report...')
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)


