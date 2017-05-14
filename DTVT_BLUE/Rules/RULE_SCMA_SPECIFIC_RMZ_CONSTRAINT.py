### ========= Template =========================================================================
from time import time
start_time = time()
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

### =========Rule RSCMA_SPECIFIC_RMZ_CONSTRAINT ===================================================================
# Author : Saleem Javed
# Updated 11 April 2017
# Caps Used : Reverse_Movement_Zones_Cap  , Points_Cap
# Constant used :  Min_RMZ_Protection ,  Min_RMR_Protection_Forward
###==================================================================================================


csv_reader = CSVReader.CSVReader(config.csv_folder_path)
SyDT = csv_reader.SyDT   
startTime = TimeoutError()
# Read Caps
rmz_cap = SyDT[csv_reader.Reverse_Movement_Zones_Cap]
point_cap = SyDT[csv_reader.Points_Cap]

rmz_id = rmz_cap['ID']
rmz_names = rmz_cap['Name']
rmz_track = rmz_cap['Track_ID']
rmz_dir = rmz_cap['Reverse_Movement_Direction']
rmz_type = rmz_cap['RMZ_Type']
rmz_kp_begin = Utility.GetKpValue(rmz_cap['Kp_BeginValue'],rmz_cap['Kp_BeginCorrected_Trolley_Value'])
rmz_kp_end =   Utility.GetKpValue(rmz_cap['Kp_EndValue'],rmz_cap['Kp_EndCorrected_Trolley_Value'])

point_name = point_cap['Name']
point_track  = point_cap['Track_ID']
point_kp_toe = Utility.GetKpValue(point_cap['Kp_ToeValue'],point_cap['Kp_ToeCorrected_Trolley_Value'])
point_kp_fouling = Utility.GetKpValue(point_cap['Kp_Fouling_PointValue'],point_cap['Kp_Fouling_PointCorrected_Trolley_Value'])

Min_RMZ_Protection = int(proj_const['Min_RMR_Protection'])
Min_RMR_Protection_Forward = int(proj_const['Min_RMR_Protection_Forward'])


# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1

Utility.WriteToWorkSheet(wsRpt,rwCount,["ID", "RMZ", "RMZ_Type","Track","Kp_Begin_Value","Kp_End_Value","Min RMR Protection Begin Up", "Min RMR Protection End Up","Min RMR Protection End Up", "Min RMR Protection End Dn", "Point ID in MIN RMR Protection Zone", "Result"])

rwCount = rwCount+1

for index in range(len(rmz_names)):
    if rmz_type[index] == 'RMR_Per_Zones':
        try:
            _result= []
            _rmz = rmz_names[index].strip()
            _rmz_kp_b = rmz_kp_begin[index]
            _rmz_kp_e = rmz_kp_end[index]
            _rmz_type = rmz_type[index]
            _rmz_track = rmz_track[index]
            _RMRUpKPb =  _rmz_kp_e
            _RMRUpKPe = _rmz_kp_e +  Min_RMZ_Protection
            _RMRDnKPb =  _rmz_kp_b - Min_RMZ_Protection
            _RMRDnKPe = _rmz_kp_b             
            _pt_failing_list = ''

            for item in range(len(point_name)):
                _pt_name = point_name[item]
                _pt_toe = point_kp_toe[item]
                _pt_flng =point_kp_fouling[item]
                _condition = ''
                                
                if point_track[item] == _rmz_track and rmz_dir[index] == "Both":
                    _condition = ( _pt_toe < _RMRUpKPb or _pt_toe > _RMRUpKPe ) and (  _pt_flng <_RMRUpKPb  or _pt_flng >_RMRUpKPe ) and ( _pt_toe > _RMRDnKPb  or _pt_toe < _RMRDnKPe ) and ( _pt_flng > _RMRDnKPb  or _pt_flng < _RMRDnKPe )
                elif point_track[item] == _rmz_track and rmz_dir[index] == "Up":
                    _condition = ( _pt_toe < _RMRUpKPb or _pt_toe > _RMRUpKPe ) and (  _pt_flng <_RMRUpKPb  or _pt_flng >_RMRUpKPe)

                elif point_track[item] == _rmz_track and rmz_dir[index] == "Down":
                    _condition = ( (_pt_toe > _RMRDnKPb ) or (_pt_toe < _RMRDnKPe )) and ( (_pt_flng > _RMRDnKPb ) or (_pt_flng < _RMRDnKPe ))

                if( _condition == True):
                    tis_log.info('RMZ:' + _rmz + ', Track: '+ _rmz_track + 'Point:'+ _pt_name+ 'passed the rule')
                    _result.append('OK')
                    global_test_results.append('OK')
                elif( _condition == False):
                    _result.append('NOK')
                    global_test_results.append('NOK')    
                    if _pt_failing_list =='':
                        _pt_failing_list = _pt_name
                    else:
                        _pt_failing_list = _pt_failing_list + ','+ _pt_name
                                   

            Utility.WriteToWorkSheet(wsRpt, rwCount, [ rmz_id[index], _rmz, _rmz_type, _rmz_track, _rmz_kp_b, _rmz_kp_e, _RMRUpKPb, _RMRUpKPe, _RMRDnKPb, _RMRDnKPe, _pt_failing_list])
            if 'NOK' in _result:
                wsRpt.cell(row = rwCount, column = 12, value = 'NOK')
                tis_log.error('RMZ:' + _rmz + ', Track: '+ _rmz_track + 'has failed the rule')
            else:
                wsRpt.cell(row = rwCount, column = 12, value = 'OK')
            rwCount = rwCount+1            

        except:
            tis_log.error( "Module:RULE_SCMA_SPECIFIC_RMZ_CONSTRAINT.py" + "Method:__main__ " +"item =" + rmz_names[index]  + "\t" ,  sys.exc_info()[0])    
            
            
for index in range(len(rmz_names)):
    if rmz_type[index] == 'RMR_Per_Zones':
        try:
            _result= []
            _rmz = rmz_names[index].strip()
            _rmz_kp_b = rmz_kp_begin[index]
            _rmz_kp_e = rmz_kp_end[index]
            _rmz_type = rmz_type[index]
            _rmz_track = rmz_track[index]
            _RMRUpKPb =  _rmz_kp_e - Min_RMR_Protection_Forward
            _RMRUpKPe = _rmz_kp_e  
            _RMRDnKPb =  _rmz_kp_b  
            _RMRDnKPe = _rmz_kp_b  + Min_RMR_Protection_Forward         
            _pt_failing_list = ''

            for item in range(len(point_name)):
                _pt_name = point_name[item]
                _pt_toe = point_kp_toe[item]
                _pt_flng =point_kp_fouling[item]
                _condition = ''
                                
                if point_track[item] == _rmz_track and rmz_dir[index] == "Both":
                    _condition = ( _pt_toe < _RMRUpKPb or _pt_toe > _RMRUpKPe ) and (  _pt_flng <_RMRUpKPb  or _pt_flng >_RMRUpKPe ) and ( _pt_toe > _RMRDnKPb  or _pt_toe < _RMRDnKPe ) and ( _pt_flng > _RMRDnKPb  or _pt_flng < _RMRDnKPe )
                elif point_track[item] == _rmz_track and rmz_dir[index] == "Up":
                    _condition = ( _pt_toe < _RMRUpKPb or _pt_toe > _RMRUpKPe ) and (  _pt_flng <_RMRUpKPb  or _pt_flng >_RMRUpKPe)

                elif point_track[item] == _rmz_track and rmz_dir[index] == "Down":
                    _condition = ( (_pt_toe > _RMRDnKPb ) or (_pt_toe < _RMRDnKPe )) and ( (_pt_flng > _RMRDnKPb ) or (_pt_flng < _RMRDnKPe ))

                if( _condition == True):
                    tis_log.info('RMZ:' + _rmz + ', Track: '+ _rmz_track + 'Point:'+ _pt_name+ 'passed the rule')
                    _result.append('OK')
                    global_test_results.append('OK')
                elif( _condition == False):
                    _result.append('NOK')
                    global_test_results.append('NOK')                    
                    if _pt_failing_list =='':
                        _pt_failing_list = _pt_name
                    else:
                        _pt_failing_list = _pt_failing_list + ','+ _pt_name                                    


            
            if 'NOK' in _result:
                Utility.WriteToWorkSheet(wsRpt, rwCount, [ rmz_id[index], _rmz, _rmz_type, _rmz_track, _rmz_kp_b, _rmz_kp_e, _RMRUpKPb, _RMRUpKPe, _RMRDnKPb, _RMRDnKPe, _pt_failing_list,'NOK'])
                rwCount = rwCount+1    
                tis_log.error('RMZ:' + _rmz + ', Track: '+ _rmz_track + 'has failed the rule')
            else:
                Utility.WriteToWorkSheet(wsRpt, rwCount, [ rmz_id[index], _rmz, _rmz_type, _rmz_track, _rmz_kp_b, _rmz_kp_e, _RMRUpKPb, _RMRUpKPe, _RMRDnKPb, _RMRDnKPe, _pt_failing_list,'OK'])
                rwCount = rwCount+1    
                    

        except:
            tis_log.error( "Module:RULE_SCMA_SPECIFIC_RMZ_CONSTRAINT.py" + "Method:__main__ " +"item =" + rmz_names[index]  + "\t" ,  sys.exc_info()[0])         

# Save Report
print('Rule Execution Finished. Saveing Report...')
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
print( "\nExecution time : " + str(time() -  start_time) + " sec.")

