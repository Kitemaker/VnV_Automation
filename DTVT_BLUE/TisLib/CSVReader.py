import os.path
import sys
import logging
from TisLib import Utility



class CSVReader(object):   
    
    def __init__(self,CsvFolderPath):
        
        self.tis_log=logging.getLogger('Tis_Logger')
        print("Creating Class CSVReader") 
        self.tis_log.info("Creating Class CSVReader") 
        self.SyDT = dict()
        self.files = [file for file in os.listdir(CsvFolderPath) if os.path.isfile(os.path.join(CsvFolderPath,file))]
       
        self.ESPs_Cap='ESPs_Cap'
        self.Points_Cap='Points_Cap'
        self.Routes_Cap='Routes_Cap'
        self.Signals_Cap='Signals_Cap'
        self.SDDB_Cap = 'SDDB_Cap'
        self.Secondary_Detection_Devices_Cap = 'Secondary_Detection_Devices_Cap'
        self.Signalisation_Areas_Cap = 'Signalisation_Areas_Cap'
        self.Switchs_Cap = 'Switchs_Cap'
        self.Tracks_Cap = 'Tracks_Cap'


        for item in self.files:            
            self.SyDT[item.split('.')[0]] = self.ReadCsvFile(os.path.join(CsvFolderPath,item))

        
    def ReadCsvFile(self,CsvFilePath):
        file_dict=dict()
        data=list()
        columns=list()
        try:
            csvfile = open(CsvFilePath,'r')     
        
            for line in csvfile:
                data.append(line.split(','))
            title_row = data[0]

            for i in range(len(title_row)):
                columns.append(list())

            for row in data:
                for c in range(len(row)):
                    columns[c].append(row[c])
 
            for i in range(len(title_row)):
                file_dict[str.rstrip(title_row[i].strip())]  = columns[i][1:]

        except FileNotFoundError:
            self.logger.error("File Not found, Please check the path" + "Module: CSVReader.py Method:ReadCsvFile") 
        except:
            self.logger.error(sys.exc_info()[0])
        finally:
            return file_dict
               
     
    def GetSDDBs(self):   
        try:
            
            return SDDB_Cap.SDDB_Cap(self.csv_folder_path +"\\"+ self.c_sddbFile)
            self.tis_log.info("Reading SDDBs from:  "+ self.csv_folder_path +"\\"+ self.c_sddbFile)
        except:
            self.tis_log.error("Module = CSVReader, Method=GetSDDBs"+ sys.exc_info()[0]) 
            return None

    def GetTracksData(self):
        try:
            self.tis_log.info("Reading Tracks from:  " + self.csv_folder_path +"\\"+ self.c_trackFile)
            return Tracks_Cap.Tracks_Cap( self.csv_folder_path  +"\\"+  self.c_trackFile)
        except:
             self.tis_log.error("Source Module: CSVReader, Method:GetTracksData"+ sys.exc_info()[0])
             return None 
    
 

    def GetRoutes(self):   
        try:
            
            return Routes_Cap.Routes_Cap(self.csv_folder_path +"\\"+ self.c_RoutesFile)
            self.tis_log.info("Reading Routess from:  "+ self.csv_folder_path +"\\"+ self.c_RoutesFile)
        except:
            self.tis_log.error("Module = CSVReader, Method = GetRoutes"+ sys.exc_info()[0]) 
            return None

    def GetPoints(self):
        try:
            return Points_Cap.Points_Cap(self.csv_folder_path +"\\"+ self.c_PointsFile)
            self.tis_log.info("Reading Points from:  "+ self.csv_folder_path +"\\"+ self.c_PointsFile)
        except:
            self.tis_log.error("Module = CSVReader, Method = GetPoints"+ sys.exc_info()[0]) 
            return None

    def GetSignalisationAreas(self):
        try:
            return Signalisation_Areas_Cap.Signalisation_Areas_Cap(self.csv_folder_path +"\\"+ self.c_SignalisationAreasFile)
            self.tis_log.info("Reading Signalisation_Areas from:  "+ self.csv_folder_path +"\\"+ self.c_SignalisationAreasFile)
        except:
            self.tis_log.error("Module = CSVReader, Method = GetSignalisationAreas "+ sys.exc_info()[0]) 
            return None

    def GetSecondaryDetectionDevices(self):
       try:
           return Secondary_Detection_Devices_Cap.Secondary_Detection_Devices_Cap(self.csv_folder_path +"\\"+ self.c_SecondaryDetectionDevicesFile)
           self.tis_log.info("Reading Signalisation_Areas from:  "+ self.csv_folder_path +"\\"+ self.c_SecondaryDetectionDevicesFile)
       except:
           self.tis_log.error("Module = CSVReader, Method = GetSecondaryDetectionDevices "+ sys.exc_info()[0]) 
           return None

    def GetSwitchs(self,CapFilePath):
       try:
           return Switchs_Cap.Switchs_Cap(self.csv_folder_path +"\\"+ self.c_SwitchsFile)
           self.tis_log.info("Reading Switchs from:  "+ self.csv_folder_path +"\\"+ self.c_SwitchsFile)
       except:
           self.tis_log.error("Module = CSVReader, Method = GetSwitchs "+ sys.exc_info()[0]) 
           return None
 
                 

    


