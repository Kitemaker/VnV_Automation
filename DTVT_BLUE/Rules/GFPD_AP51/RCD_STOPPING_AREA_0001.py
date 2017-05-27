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

### =========RCD_STOPPING_AREA_0001===============================================================
# Author : Saleem Javed
# Updated 23 May 2017
# Caps Used : Sydb Nodes Platforms,Change_Of_Direction_Areas,Stablings_Location,Isolation_Areas
#                        Coupling_Uncoupling_Areas,Washing_Zones,Transfer_Tracks,
# Constant used :  None 
# GFPD : 0962_AP51
###================================================================================================

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Stopping_Area", "Original_Area_Name", "Original_Area_SSP_Ids","Result"])
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

def GetOriginalSSPId(OriginalArea:dict, ID):
    try:
        for name, items in OriginalArea.items():
            if int(ID) == int(items['ID']):
                return [name,items['SSP_ID_List']]
    except:
        self.dtvt_log.error("Module:RULE_STOPPING_AREA_0008 Method:GetOriginalSSPId", sys.exc_info()[0])

for sta, orig_area_list in stopping_areas.items():
    _org_name_list=[]
    _sta_name = sta
    _sta_track= []   
    
    _result = ''
    _org_name = ''
    _org_ssp_id_list = list()
    for _org_area in orig_area_list:
        _org_id = _org_area.split(';')[0]
        _org_area_type = _org_area.split(';')[1]

        if _org_area_type == 'Change Of Direction Area':
            _org_values = GetOriginalSSPId(cod_area,_org_id)
        elif _org_area_type == 'Platform':
            _org_values = GetOriginalSSPId(platforms,_org_id)
        elif _org_area_type == 'Stabling':
            _org_values = GetOriginalSSPId(stablings,_org_id)

        elif _org_area_type == 'Coupling Uncoupling':
            _org_values = GetOriginalSSPId(coupling_areas,_org_id)

        elif _org_area_type == 'Washing':
            _org_values = GetOriginalSSPId(wasing_zones,_org_id)

        elif _org_area_type == 'Transfer Track':
            _org_values = GetOriginalSSPId(transfer_tracks,_org_id)

        elif _org_area_type == 'Isolation Area':
            _org_values = GetOriginalSSPId(isolation_areas,_org_id)

        if(_org_values != None):
            _org_name   =  _org_values[0]
            _org_ssp_id_list = _org_values[1]

            if( len(_org_ssp_id_list) >=1):
                _result = 'OK' 
                global_test_results.append('OK')       
                dtvt_log.info(_sta_name +'\t'+ _org_name +'\t'  +  Utility.ConvertToString(_org_ssp_id_list))
            else:
                _result = 'NOK'  
                global_test_results.append('NOK')      
                dtvt_log.error(_sta_name +'\t'+ _org_name +'\t' + Utility.ConvertToString(_org_ssp_id_list))

            Utility.WriteToWorkSheet(wsRpt,rwCount,[_sta_name,_org_name,Utility.ConvertToString(_org_ssp_id_list),_result])
            rwCount = rwCount+1


# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
