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

### ======== Template Ends===========================================================================

### =========Rule TMS_SSP_0012 ===================================================================
# Author : Saleem Javed
# Updated 4 May 2017
# Caps Used : Service_Stopping_Points_Cap  , TRFC_Cap,Lines_Cap,Platforms_Cap,Stablings_Location_Cap,SDDB_Cap
# Constant used :  Line.Min_Head_Opposite_Shunting_Axle_Vehicle_Length , Local_D_Joint, Loc_Error_Platform,Loc_Error_Stabling,Loc_Error_Others, Stopping_accuracy
 
###==================================================================================================

 

# Read Caps
ssp_cap = SyDT['Service_Stopping_Points_Cap']
trfc_cap = SyDT['TRFC_Cap']
sddb_cap = SyDT['SDDB_Cap']
lines_cap = SyDT['Lines_Cap']
platforms_cap = SyDT['Platforms_Cap']
stablings_cap = SyDT['Stablings_Location_Cap']
sddb_cap = SyDT['SDDB_Cap']

ssp_name = ssp_cap['Name']
ssp_track = ssp_cap['Track_ID']
ssp_kp = Utility.GetKpValue(ssp_cap['KpValue'],ssp_cap['KpCorrected_Trolley_Value'])
ssp_direction =  ssp_cap['Direction']
ssp_trains = ssp_cap['Train_Formation_Characteristics_ID_List']

Min_Head_Opposite_Shunting_Axle_Vehicle_Length = int(str.strip(lines_cap['Min_Head_Opposite_Shunting_Axle_Vehicle_Length'][0]))

trfc_name = trfc_cap['Name']
trfc_length = trfc_cap['Formation_Length']

sddb_name = sddb_cap['Name']
sddb_kp = Utility.GetKpValue(sddb_cap['KpValue'],sddb_cap['KpCorrected_Trolley_Value'])
sddb_track = sddb_cap['Track_ID']

track_directions = Utility.GetTrackDirections(Utility.GetTrackDirectionFile(root_folder))

local_D_Joint = int(str.strip(proj_const['Local_D_Joint']))
stopping_accuracy = int(str.strip(proj_const['Stopping_Accuracy']))

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["SSP","SSP_Kp","Stopping_Accuracy","Loc_Error","Local_D_Joint","TRFC","Formation_Length","SDDB_Kp","Result"])
rwCount = rwCount+1

# Logic Starts Here

for index in range(len(ssp_name)):
    _ssp = ssp_name[index]
    _ssp_kp = ssp_kp[index]
    _ssp_dir = ssp_direction[index]
    _ssp_type = Utility.GetSSPType(_ssp, platforms_cap['SSP_ID_List'],stablings_cap['SSP_ID_List'])
    _ssp_trfc = ssp_trains[index]
    _ssp_track = ssp_track[index]
    _track_sddbkp_List = list()
    _res = ""
     
    if _ssp_type == 'Platform':
        _loc_error = proj_const['Loc_Error_Platform']
    elif  _ssp_type == 'Stabling':
        _loc_error = proj_const['Loc_Error_Stabling']
    else:
        _loc_error = proj_const['Loc_Error_Others']  

    for item in range(len(sddb_track)):
        if sddb_track[item] == _ssp_track:
            _track_sddbkp_List.append(sddb_kp[item])

    _track_dir_incr_kp = track_directions[_ssp_track]
    if str.upper(_track_dir_incr_kp) == 'DOWN' and str.upper(_ssp_dir) == 'UP':
        _ssp_sddb_kp = Utility.GetNearestTailSDDBForSSP(_ssp_kp,'DOWN',_track_sddbkp_List)
    elif str.upper(_track_dir_incr_kp) == 'DOWN' and str.upper(_ssp_dir) == 'DOWN':
        _ssp_sddb_kp = Utility.GetNearestTailSDDBForSSP(_ssp_kp,'UP',_track_sddbkp_List)
    else:
        _ssp_sddb_kp = Utility.GetNearestTailSDDBForSSP(_ssp_kp,_ssp_dir,_track_sddbkp_List)


    for train in _ssp_trfc.split(';'):
        _tr_length = int(trfc_length[trfc_name.index(train)])
        dist_A = abs(_ssp_kp - _ssp_sddb_kp) - _tr_length
        dist_B = Min_Head_Opposite_Shunting_Axle_Vehicle_Length - local_D_Joint - stopping_accuracy - int(_loc_error)

        if dist_A < dist_B :
            _res = "OK"
            global_test_results.append(_res)
        else:
            _res = "NOK"
            global_test_results.append(_res)
            dtvt_log.error("Test Fails for SSP: " + _ssp + "Train: " + train )

        Utility.WriteToWorkSheet(wsRpt,rwCount,[_ssp,_ssp_kp,stopping_accuracy,_loc_error,local_D_Joint,train,_tr_length,_ssp_sddb_kp,_res])
        rwCount = rwCount+1           
       

 # Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)    
        