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
SyDB             = param['SyDB']

### ======== Template Ends=========================================================================

### =========RULE_STOPPING_AREA_0008===============================================================
# Author : Saleem Javed
# Updated 23 May 2017
# Caps Used : Sydb Nodes Platforms,Change_Of_Direction_Areas,Stablings_Location,Isolation_Areas
#                        Coupling_Uncoupling_Areas,Washing_Zones,Transfer_Tracks,
# Constant used :  None 
# GFPD : 0962_AR
###================================================================================================

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Stopping_Area", "Original_Area_Names", "Original_Area_Tracks", "Original_Area_Kp_Begin", "Original_Area_Kp_End","Result"])
rwCount = rwCount+1

# Read Caps
stopping_areas = dict(SyDB.Get_Stopping_Areas())
cod_area = dict(SyDB.Get_COD_Areas_With_Items())
platforms = dict(SyDB.Get_Platforms_With_Items())
stablings = dict(SyDB.Get_Stabling_Location_With_Items())
coupling_areas = dict(SyDB.Get_Coupling_Uncoupling_Area_With_Items())
wasing_zones = dict(SyDB.Get_Washing_Zone_With_Items())
transfer_tracks = dict(SyDB.Get_Transfer_Tracks_With_Items())
isolation_areas = dict(SyDB.Get_Isolation_Areas_With_Items())

def GetOriginalAreaItems(OriginalArea:dict, ID):
    try:
        for name, items in OriginalArea.items():
            if int(ID) == int(items['ID']):
                return [name,items['Track_ID'],items['Kp_Begin'],items['Kp_End']]
    except:
        self.dtvt_log.error("Module:RULE_STOPPING_AREA_0008 Method:GetOriginalAreaItems", sys.exc_info()[0])

for sta, orig_area_list in stopping_areas.items():
    _org_name_list=[]
    _sta_name = sta
    _sta_track= []
    _sta_kp_begin = []
    _sta_kp_end = []
    _result = ''
    for _org_area in orig_area_list:
        _org_id = _org_area.split(';')[0]
        _org_area_type = _org_area.split(';')[1]

        if _org_area_type == 'Change Of Direction Area':
            _org_values = GetOriginalAreaItems(cod_area,_org_id)
        elif _org_area_type == 'Platform':
            _org_values = GetOriginalAreaItems(platforms,_org_id)
        elif _org_area_type == 'Stabling':
            _org_values = GetOriginalAreaItems(stablings,_org_id)

        elif _org_area_type == 'Coupling Uncoupling':
            _org_values = GetOriginalAreaItems(coupling_areas,_org_id)

        elif _org_area_type == 'Washing':
            _org_values = GetOriginalAreaItems(wasing_zones,_org_id)

        elif _org_area_type == 'Transfer Track':
            _org_values = GetOriginalAreaItems(transfer_tracks,_org_id)

        elif _org_area_type == 'Isolation Area':
            _org_values = GetOriginalAreaItems(isolation_areas,_org_id)

        if(_org_values != None):
            _org_name_list.append(_org_values[0])
            _sta_track.append(_org_values[1])
            _sta_kp_begin.append(_org_values[2])
            _sta_kp_end.append(_org_values[3])


    _sta_track_set = set(_sta_track)
    _sta_kp_begin_set = set(_sta_kp_begin)
    _sta_kp_end_set = set(_sta_kp_end)

    if( len(_sta_track_set) ==1 and len(_sta_kp_begin_set) == 1 and len (_sta_kp_end_set) ==1 ):
        _result = 'OK' 
        global_test_results.append('OK')       
        dtvt_log.info(_sta_name + Utility.ConvertToString(_org_name_list) +'\t'+ Utility.ConvertToString( _sta_track) + '\t'+ 'KpBegin = ' + Utility.ConvertToString( _sta_kp_begin) +'\tKpEnd '+ Utility.ConvertToString( _sta_kp_end))
    else:
        _result = 'NOK'  
        global_test_results.append('NOK')      
        dtvt_log.error(_sta_name + Utility.ConvertToString(_org_name_list) +'\t'+ Utility.ConvertSetToString( _sta_track) + '\t'+ 'KpBegin = ' + Utility.ConvertSetToString( _sta_kp_begin) +'\tKpEnd '+ Utility.ConvertSetToString( _sta_kp_end))

    Utility.WriteToWorkSheet(wsRpt,rwCount,[_sta_name,Utility.ConvertToString(_org_name_list),Utility.ConvertToString(_sta_track),
                              Utility.ConvertToString(_sta_kp_begin),Utility.ConvertToString(_sta_kp_end),_result])
    rwCount = rwCount+1


# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
