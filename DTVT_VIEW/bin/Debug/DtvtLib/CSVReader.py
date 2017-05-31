import os.path
import sys
import logging
from DtvtLib import Utility



class CSVReader(object):   
    
    def __init__(self,CsvFolderPath):
        
        self.dtvt_log=logging.getLogger('Dtvt_Logger')
        print("Creating Class CSVReader") 
        self.dtvt_log.info("Creating Class CSVReader") 
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
        self.Service_Stopping_Points_Cap='Service_Stopping_Points_Cap'
        self.Platforms_Cap = 'Platforms_Cap'
        self.TRFC_Cap = 'TRFC_Cap'
        self.Lines_Cap = 'Lines_Cap'
        self.Platforms_Cap = 'Platforms_Cap'
        self.Stablings_Location_Cap = 'Stablings_Location_Cap'
        self.Reverse_Movement_Zones_Cap = 'Reverse_Movement_Zones_Cap'


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
            
            # remove any whitespace 
            for key,value in file_dict.items():
                for item in value:
                    item = item.strip()
                    item = item.rstrip()

        except FileNotFoundError:
            self.logger.error("File Not found, Please check the path" + "Module: CSVReader.py Method:ReadCsvFile") 
        except:
            self.logger.error(sys.exc_info()[0])
        finally:
            return file_dict