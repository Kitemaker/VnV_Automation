import os
import sys
import logging
import xml.dom.minidom as dom
import xml.etree.ElementTree as ET
import DtvtLib.Utility

class Configuration(object):
    """Configuration of the project"""
    def __init__(self, Root_Folder_Path):
        self.Dtvt_logger = logging.getLogger('Dtvt_Logger')
        try:
            self.root_folder_path = Root_Folder_Path
            self.config_File_Path = self.root_folder_path + "\\Configuration\\Configuration.xml"
            self.csv_folder_path =  self.root_folder_path + "\\Input\\Csv_Files"
            self.csv_files=dict()
            # Decalare variables
            self.project_name = ''
            self.project_baseline = ''
            self.uevol_baseline = ''
            self.database_baseline = ''
            self.sydt_version = ''
            self.sydb_file_path = ''
            self.C_Late_Change_Distance_File_Path = ''
            # read Configuration.xml
            self.__readConfiguration(self.config_File_Path)
            # read CSV File Names
            self.__readCsvFileNames(self.csv_folder_path)
           


        except:
            self.Dtvt_logger.error("Module: Configuration.py" , sys.exc_info()[0] )
    
    def __readConfiguration(self,ConfigFile):
        """read conig.xml file"""
        try:

            config=ET.parse(ConfigFile)
            root_node = config.getroot()
            
            self.project_name= root_node.attrib['name']
            self.project_baseline=root_node.attrib['baseline']
            self.project_name=root_node.attrib['name']
            self.uevol_baseline=root_node.attrib['uevol_baseline']
            self.database_baseline=root_node.attrib['database_baseline']
            self.sydt_version=root_node.attrib['sydt_version']
            self.C_Late_Change_Distance_File_Path = root_node.find('C_Late_Change_Distance').attrib['path']
            self.sydb_file_path = root_node.find('SyDB').attrib['path']
        except:
            self.dtvt_logger.error( sys.exc_info()[0] + "Module: Configuration.py" + "Method:ReadConfiguration")


    def __readCsvFileNames(self,CsvFolderPath):
        """read the CSV file names and create dictionalry with file paths"""
        try:

            csvFiles =[ item for item in os.listdir(CsvFolderPath) if ( os.path.isfile(os.path.join(CsvFolderPath,item)) and item.split('.')[1] == 'csv')]
            self.csv_files={file:os.path.join(CsvFolderPath,file) for file  in csvFiles}

        except:
            self.dtvt_logger.error( sys.exc_info()[0] + "Module: Configuration.py" + "Method:ReadCsvFileNames")
        