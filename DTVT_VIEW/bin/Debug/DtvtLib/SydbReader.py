import os.path
import sys
import xml.etree.ElementTree as ET
import logging


class SydbReader(object):
    
    def __init__(self, SydbPath):
        print('Creating SyDB Reader')
        self.sydb_file = ET.parse(SydbPath)
        self.root_node = self.sydb_file.getroot()
        self.Tool_Version =  self.root_node.attrib['Tool_Version']
        self.Sector_ID = self.root_node.attrib['Sector_ID']
        self.SyPD_Version = self.root_node.attrib['SyPD_Version']
        self.XML_File_Version = self.root_node.attrib['XML_File_Version']        
        self.dtvt_log =  logging.getLogger('Dtvt_Logger')
        self.DL1 = self.GetFirsLevelItemNames()
        self.DL2 = self.GetSecondLevelItems()
        self.data_tables = dict()

    def GetFirsLevelItemNames(self):
        data_Level1=dict()
        try:
            data_Level1 = {item.tag : item  for item in self.root_node.getchildren()}

            return data_Level1
        except:
            self.dtvt_log.error((sys.exc_info()[0]))
            return None

    def GetSecondLevelItems(self):
        data_Level2=dict()
        try:
            for nodeName, node in self.DL1.items():
                data_Level2[nodeName] = node.getchildren()

            return data_Level2
        except:
            self.dtvt_log.error((sys.exc_info()[0]))
            return None

    def GetDataTables(self):
        dts = dict()
        eqpdts = dict()
        for item in self.root_node.getchildren():
            eqps = item.getchildren()
            for k,v in eqps[0].attrib.items():
                eqpdts[k] = ''
            for key,value in eqpdts:
                eqpdts[k] = [item.attrib[k] for item in eqps]
            dts[item.tag] = eqpdts
        return dts

    def Point_Deadlocking_Block_ID_List(self):
        deadlocking_block_id_list = dict()
        try:
            point_list = self.root_node.findall('./Points/Point')
            for point in point_list:
                pt_name = point.attrib['Name']           
                deadlocking_block_id_list[pt_name]= [int(bl.text) for bl in point.findall('./Deadlocking_Block_ID_List/Block_ID')]           
        except:
            self.dtvt_log.error("Module:SydbReader Method:Point_Deadlocking_Block_ID_List", sys.exc_info()[0])
            deadlocking_block_id_list = None
        finally:
            return deadlocking_block_id_list

    def Get_Route_OriginSignal_Pairs(self):
        route_signal_pairs = dict()
        try:
            for route in self.root_node.findall('./Routes/Route'):
                route_signal_pairs[route.attrib['Name']] = route.find('Origin_Signal_ID').text
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Route_OriginSignal_Pair", sys.exc_info()[0])
            return None
        finally:
            return route_signal_pairs

    def Get_Signal_ID_Kp_Pairs(self):
        signal_id_kp_pairs = dict()
        try:
            for signal in self.root_node.findall('./Signals/Signal'):
                kp_node = signal.find('Kp')
                signal_id_kp_pairs[signal.attrib['ID']] = int(kp_node.attrib['Value']) + int(kp_node.attrib['Corrected_Gap_Value']) +  int(kp_node.attrib['Corrected_Trolley_Value'])
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Signal_ID_Kp_Pairs", sys.exc_info()[0])
            return None
        finally:
            return signal_id_kp_pairs


    def Get_Switch_Points_Pairs(self):
        try:
            switch_points_pairs = dict()
            for sw in self.root_node.findall('./Switchs/Switch'):
                sw_id = sw.attrib['ID']
                conv_pts = sw.findall('./Convergent_Point_ID_List/Convergent_Point_ID')
                div_pts =  sw.findall('./Divergent_Point_ID_List/Divergent_Point_ID')
                switch_points_pairs[sw_id] = [item.text for item in (conv_pts + div_pts)]
            return switch_points_pairs
        except:
             self.dtvt_log.error("Module:SydbReader Method:Get_Switch_Points_Pairs", sys.exc_info()[0])
             return None


    def Get_Route_Points_Pairs(self):
        try:
            route_points_pair = dict()
            switch_pt_pairs = self.Get_Switch_Points_Pairs()
            for route in self.root_node.findall('./Routes/Route'):
                ptList = list()                     
                for switch in route.findall('./Switch_ID_List/Switch_ID'):
                    ptList.extend(switch_pt_pairs[switch.text])

                route_points_pair[route.attrib['Name']] = ptList
            return route_points_pair
        except:

             self.dtvt_log.error("Module:SydbReader Method:Get_Route_Points_Pairs", sys.exc_info()[0])
             return None


    def Get_Point_ID_Name_Pairs(self):
        try:
            point_id_name_pair = dict()            
            for point in self.root_node.findall('./Points/Point'):
                point_id_name_pair[point.attrib['ID']] = point.attrib['Name']
            return point_id_name_pair
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Point_ID_Name_Pairs", sys.exc_info()[0])
            return None

    def Get_Switch_ID_Name_Pairs(self):
        try:
            switch_id_name_pair = dict()            
            for sw in self.root_node.findall('./Switchs/Switch'):
                switch_id_name_pair[sw.attrib['ID']] = sw.attrib['Name']
            return switch_id_name_pair
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Switch_ID_Name_Pairs", sys.exc_info()[0])
            return None

    def Get_Signals_ID_Name_Pairs(self):
        try:
            sig_id_name_pair = dict()            
            for sig in self.root_node.findall('./Signals/Signal'):
                sig_id_name_pair[sig.attrib['ID']] = sig.attrib['Name']
            return sig_id_name_pair
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Signals_ID_Name_Pairs", sys.exc_info()[0])
            return None
    def Get_Signals_ID_BlockID_Pairs(self):
        """
        Returns  dictionary of Singnal ID (int) and Block ID (int)
        """
        try:
            sig_id_blk_pair = dict()
            sig_id_kp_pair = self.Get_Signal_ID_Kp_Pairs()          
            for sig in self.root_node.findall('./Signals/Signal'):
                sig_kp = sig_id_kp_pair[sig.attrib['ID']]
                for block in self.root_node.findall('./Blocks/Block'):
                    if sig.find('Track_ID').text == block.find('Track_ID').text:
                        kp_begin = block.find('Kp_Begin').text
                        kp_end   = block.find('Kp_End').text
                        temp = list([int(kp_begin),int(kp_end),sig_kp])
                        temp.sort()
                        if temp.index(sig_kp) ==1:
                            sig_id_blk_pair[int(sig.attrib['ID'])] = int(block.attrib['ID'])
                            break          
                
            return sig_id_blk_pair
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Signals_ID_BlockID_Pairs", sys.exc_info()[0])
            return None

    def Get_Stopping_Areas(self):
        """"
        Returns dictionary of Stopping_Areas 
        output Key   : Stopping_Area Name
        output Value : List of pairs of Original_Area_ID & Original_Area_Type  e.g. [ID1;Original_Area_Type1 ,ID2; Original_Area_Type2....]
        """
        _stopping_areas = dict()
        try:

            for _sta in self.root_node.findall('./Stopping_Areas/Stopping_Area'):
                _orig_areal_list = []
                _name = ''
                _name = _sta.attrib['Name']
                if(_name != ''):
                    for _org in _sta.findall('./Original_Area_List/Original_Area'):
                        _orig_areal_list.append(_org.attrib['ID'] + ";" + _org.attrib['Original_Area_Type'])

                    _stopping_areas[_name] = _orig_areal_list
            return _stopping_areas
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Stopping_Areas", sys.exc_info()[0])
            return None

    def Get_Platforms_With_Items(self):
        """ Return dict of Platform Name and its Child Nodes in dict fomrat """
        try:
            _platforms = dict()
            for _ptf in self.root_node.findall('./Platforms/Platform'):     
                           
                platform_items = dict()
                platform_items['ID'] = int(_ptf.attrib['ID'])
                platform_items['Track_ID'] = _ptf.find('Track_ID').text
                platform_items['SSP_ID_List'] = self.Get_SSP_ID_List(_ptf)
                _kp_beg =  _ptf.find('Kp_Begin')
                _kp_end =  _ptf.find('Kp_End')
                platform_items['Kp_Begin'] = int(_kp_beg.attrib['Value']) +   int(_kp_beg.attrib['Corrected_Gap_Value']) +  int(_kp_beg.attrib['Corrected_Trolley_Value'])
                platform_items['Kp_End'] = int(_kp_end.attrib['Value']) +   int(_kp_end.attrib['Corrected_Gap_Value']) +  int(_kp_end.attrib['Corrected_Trolley_Value'])
                _platforms[_ptf.attrib['Name']] = platform_items


            return _platforms
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Platforms_With_Items", sys.exc_info()[0])
            return None

    def Get_COD_Areas_With_Items(self):

        """ Return dict of COD_Area Name and its Child Nodes in dict fomrat """
        try:
            _cod_areas = dict()
            for _cod in self.root_node.findall('./Change_Of_Direction_Areas/Change_Of_Direction_Area'):     
                           
                _cod_items = dict()
                _cod_items['ID'] = int(_cod.attrib['ID'])
                _cod_items['Track_ID'] = _cod.find('Track_ID').text
                _cod_items['SSP_ID_List'] = self.Get_SSP_ID_List(_cod)
                _kp_beg =  _cod.find('Kp_Begin')
                _kp_end =  _cod.find('Kp_End')
                _cod_items['Kp_Begin'] = int(_kp_beg.attrib['Value']) +   int(_kp_beg.attrib['Corrected_Gap_Value']) +  int(_kp_beg.attrib['Corrected_Trolley_Value'])
                _cod_items['Kp_End'] = int(_kp_end.attrib['Value']) +   int(_kp_end.attrib['Corrected_Gap_Value']) +  int(_kp_end.attrib['Corrected_Trolley_Value'])
                _cod_areas[_cod.attrib['Name']] = _cod_items


            return _cod_areas
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Platforms_With_Items", sys.exc_info()[0])
            return None

    def Get_Stabling_Location_With_Items(self):

        """ Return dict of Stabling_Location Name and its Child Nodes in dict fomrat """
        try:
            _stl_locations = dict()
            for _stl in self.root_node.findall('./Stablings_Location/Stabling_Location'):     
                           
                _stl_items = dict()
                _stl_items['ID'] = int(_stl.attrib['ID'])
                _stl_items['Track_ID'] = _stl.find('Track_ID').text
                _stl_items['SSP_ID_List'] = self.Get_SSP_ID_List(_stl)
                _kp_beg =  _stl.find('Kp_Begin')
                _kp_end =  _stl.find('Kp_End')
                _stl_items['Kp_Begin'] = int(_kp_beg.attrib['Value']) +   int(_kp_beg.attrib['Corrected_Gap_Value']) +  int(_kp_beg.attrib['Corrected_Trolley_Value'])
                _stl_items['Kp_End'] = int(_kp_end.attrib['Value']) +   int(_kp_end.attrib['Corrected_Gap_Value']) +  int(_kp_end.attrib['Corrected_Trolley_Value'])
                _stl_locations[_stl.attrib['Name']] = _stl_items


            return _stl_locations
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Stabling_Location_With_Items", sys.exc_info()[0])
            return None

    def Get_Coupling_Uncoupling_Area_With_Items(self):

        """ Return dict of Coupling_Uncoupling_Area Name and its Child Nodes in dict fomrat """
        try:
            _coupling_areas = dict()
            for _cpl in self.root_node.findall('./Coupling_Uncoupling_Areas /Coupling_Uncoupling_Area'):     
                           
                _coupling_items = dict()
                _coupling_items['ID'] = int(_cpl.attrib['ID'])
                _coupling_items['Track_ID'] = _cpl.find('Track_ID').text
                _coupling_items['SSP_ID_List'] = self.Get_SSP_ID_List(_cpl)
                _kp_beg =  _cpl.find('Kp_Begin')
                _kp_end =  _cpl.find('Kp_End')
                _coupling_items['Kp_Begin'] = int(_kp_beg.attrib['Value']) +   int(_kp_beg.attrib['Corrected_Gap_Value']) +  int(_kp_beg.attrib['Corrected_Trolley_Value'])
                _coupling_items['Kp_End'] = int(_kp_end.attrib['Value']) +   int(_kp_end.attrib['Corrected_Gap_Value']) +  int(_kp_end.attrib['Corrected_Trolley_Value'])

                _coupling_areas[_cpl.attrib['Name']] = _coupling_items


            return _coupling_areas
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Coupling_Uncoupling_Area_With_Items", sys.exc_info()[0])
            return None

    def Get_Washing_Zone_With_Items(self):

        """ Return dict of Washing_Zone Name and its Child Nodes in dict fomrat """
        try:
            _washing_zones = dict()
            for _wsh in self.root_node.findall('./Washing_Zones/Washing_Zone'):     
                           
                _washing_items = dict()
                _washing_items['ID'] = int(_wsh.attrib['ID'])
                _washing_items['Track_ID'] = _wsh.find('Track_ID').text
                _washing_items['SSP_ID_List'] = self.Get_SSP_ID_List(_wsh)
                _kp_beg =  _wsh.find('Kp_Begin')
                _kp_end =  _wsh.find('Kp_End')
                _washing_items['Kp_Begin'] = int(_kp_beg.attrib['Value']) +   int(_kp_beg.attrib['Corrected_Gap_Value']) +  int(_kp_beg.attrib['Corrected_Trolley_Value'])
                _washing_items['Kp_End'] = int(_kp_end.attrib['Value']) +   int(_kp_end.attrib['Corrected_Gap_Value']) +  int(_kp_end.attrib['Corrected_Trolley_Value'])
                _washing_zones[_wsh.attrib['Name']] = _washing_items


            return _washing_zones
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Washing_Zone_With_Items", sys.exc_info()[0])
            return None
    
    def Get_Transfer_Tracks_With_Items(self):

        """ Return dict of Transfer_Track Name and its Child Nodes in dict fomrat """
        try:
            _transfer_tracks = dict()
            for _tfr in self.root_node.findall('./Transfer_Tracks/Transfer_Track'):     
                           
                _transfer_items = dict()
                _transfer_items['ID'] = int(_tfr.attrib['ID'])
                _transfer_items['Track_ID'] = _tfr.find('Track_ID').text
                _transfer_items['SSP_ID_List'] = self.Get_SSP_ID_List(_tfr)
                _kp_beg =  _tfr.find('Kp_Begin')
                _kp_end =  _tfr.find('Kp_End')
                _transfer_items['Kp_Begin'] = int(_kp_beg.attrib['Value']) +   int(_kp_beg.attrib['Corrected_Gap_Value']) +  int(_kp_beg.attrib['Corrected_Trolley_Value'])
                _transfer_items['Kp_End'] = int(_kp_end.attrib['Value']) +   int(_kp_end.attrib['Corrected_Gap_Value']) +  int(_kp_end.attrib['Corrected_Trolley_Value'])
                _transfer_tracks[_tfr.attrib['Name']] = _transfer_items


            return _transfer_tracks
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Transfer_Tracks_With_Items", sys.exc_info()[0])
            return None

    def Get_Isolation_Areas_With_Items(self):

        """ Return dict of Washing_Zone Name and its Child Nodes in dict fomrat """
        try:
            _isolation_areas = dict()
            for _iso in self.root_node.findall('./Isolation_Areas/Isolation_Area'):     
                           
                _isolation_items = dict()
                _isolation_items['ID'] = int(_iso.attrib['ID'])
                _isolation_items['Track_ID'] = _iso.find('Track_ID').text
                _isolation_items['SSP_ID_List'] = self.Get_SSP_ID_List(_iso)
                _kp_beg =  _iso.find('Kp_Begin')
                _kp_end =  _iso.find('Kp_End')
                _isolation_items['Kp_Begin'] = int(_kp_beg.attrib['Value']) +   int(_kp_beg.attrib['Corrected_Gap_Value']) +  int(_kp_beg.attrib['Corrected_Trolley_Value'])
                _isolation_items['Kp_End'] = int(_kp_end.attrib['Value']) +   int(_kp_end.attrib['Corrected_Gap_Value']) +  int(_kp_end.attrib['Corrected_Trolley_Value'])
                _isolation_areas[_iso.attrib['Name']] = _isolation_items


            return _isolation_areas
        except:
            self.dtvt_log.error("Module:SydbReader Method:Get_Isolation_Areas_With_Items", sys.exc_info()[0])
            return None

    def Get_SSP_ID_List(self,InElement):
        try:
            ssp_id_list = list()            
            for item in InElement.findall('./SSP_ID_List/SSP_ID'):
                ssp_id_list.append(item.text)

            return ssp_id_list
        except:
            elf.dtvt_log.error("Module:SydbReader Method:Get_SSP_ID_List", sys.exc_info()[0])
            return None
           

    


