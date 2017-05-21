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

### =========Rule RCD_DB_SIGAREA_0003 ===================================================================
# Author : Saleem Javed
# Updated 16 May 2017
# Caps Used : Signalisation_Areas_Cap , Points_Cap , SDDBs_Cap,Secondary_Detection_Devices_Cap
# Constant used : Head_Correction,  NIAP_Tail_Correction 
###==================================================================================================

protected_dist = max(int(proj_const['Head_Correction']) ,int(proj_const['NIAP_Tail_Correction']))

# Read Caps
points_cap = SyDT['Points_Cap']
sig_area_cap = SyDT['Signalisation_Areas_Cap']
sddb_cap = SyDT['SDDB_Cap']
sdd_cap = SyDT['Secondary_Detection_Devices_Cap']

sig_area_name = sig_area_cap['Name']
sig_area_sdd_list = sig_area_cap['Area_Boundary_Secondary_Detection_Device_ID_List']

sdd_name = sdd_cap['Name']
sdd_sddb_list = sdd_cap['Secondary_Detection_Device_Boundary_ID_List']

sddb_name = sddb_cap['Name']
sddb_track = sddb_cap['Track_ID']
sddb_kp = Utility.SDDBKp(sddb_cap)

points_name = points_cap['Name']
points_track = points_cap['Track_ID']
points_kp_toe = Utility.GetKpValue(points_cap['Kp_ToeValue'],points_cap['Kp_ToeCorrected_Trolley_Value'])


# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["ZC", "Adjacent ZC", "SDDB", "SDDB_Track", "SDDB_Kp","Kp1","kp2", "Point","Point_Kp_Toe","Result"])
rwCount = rwCount+1
zc_sddbs = dict()

for index in range(len(sig_area_name)):
    try: 
        if(sig_area_cap['Area_Type'][index] == 'ZC'):
            _result = ""
            _zc_name = sig_area_name[index]
            _temp_sddb_list = list()
            for _sdd in sig_area_sdd_list[index].split(';'):
                _sdd = str.strip(_sdd)                
                for _sddb in sdd_sddb_list[sdd_name.index(_sdd)].split(';'):
                    _sddb = str.strip(_sddb)                    
                    _temp_sddb_list.append(_sddb)
            zc_sddbs[_zc_name] = set(_temp_sddb_list)
    except:
        dtvt_log.error( "Module:RULE_DB_ROUTE_0001.py" + "Method:__main__ " +"item =" + str(index )+ "\t" , sys.exc_info()[0])     


for zc , sddb_list in zc_sddbs.items():
    for index in range(len(sig_area_name)):
        if(sig_area_cap['Area_Type'][index] == 'ZC') and ( sig_area_name[index] != zc):
            for sdd1 in sddb_list:
                if sdd1 in zc_sddbs[sig_area_name[index]]:
                    _sddb_kp = sddb_kp[sddb_name.index(sdd1)]
                    kp1 = _sddb_kp + protected_dist
                    kp2 = _sddb_kp - protected_dist
                    #print(zc + '\t' + sig_area_name[index] + '\t'+ sdd1 +'\t'+ str(_sddb_kp) + '\t'+ str(kp1)+ '\t' + str(kp2) )
                    for i in range(len(points_name)):
                        _result = ''
                        _pt_name = points_name[i]
                        _pt_track = points_track[i]
                        _pt_kp_toe = points_kp_toe[i]
                        if(_pt_track == sddb_track[sddb_name.index(sdd1)]):
                            kp_list = [kp1,kp2,_pt_kp_toe]
                            kp_list.sort()
                            if(kp_list.index(_pt_kp_toe) ==1):
                                _result = 'NOK'          
                                global_test_results.append('NOK')     
                                dtvt_log.error(zc +  '\t' + sig_area_name[index] + '\t' + sdd1 + '\t' + sddb_track[sddb_name.index(sdd1)] +'\t' + str(_sddb_kp)+'\t' + str(kp1) + '\t' + str(kp2)+ '\t'+ _pt_name +'\t' +str(_pt_kp_toe) +'\t' +_result)                 
                            else:
                                _result = 'OK'
                                global_test_results.append('OK')    

                            Utility.WriteToWorkSheet(wsRpt,rwCount,[zc , sig_area_name[index] , sdd1 , sddb_track[sddb_name.index(sdd1)] , str(_sddb_kp),str(kp1),str(kp2), _pt_name ,str(_pt_kp_toe) ,_result])
                            rwCount = rwCount+1




       

# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
