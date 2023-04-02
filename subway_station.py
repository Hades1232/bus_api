import requests
import urllib.parse
import json
from typing import Literal


with open("key.json", "r") as f:
    data = json.load(f)

SERVICE_KEY = data["api_key"]



class SubwayStation:

    def __init__(self, page_no : str = "1", num_of_rows : str = "10", return_type : Literal["json", "xml"] = "json") -> None:
        self.endpoint_url = "https://apis.data.go.kr/1613000/SubwayInfoService"
        self.service_key = SERVICE_KEY
        self.page_no = page_no
        self.num_of_rows = num_of_rows
        self.return_type = return_type

        
    def get_station_id_by_keyword(self, staion_name : str) -> dict[str, str | list[dict[str, str]] | None]:
        url = self.endpoint_url + "/getKwrdFndSubwaySttnList?"
        payload_dic = {"serviceKey" : self.service_key, "subwayStationName" : staion_name, "pageNo" : self.page_no, "numOfRows" : self.num_of_rows, "_type" : self.return_type}
        
        encoded_payload_dic = urllib.parse.urlencode(payload_dic, safe="%&")
        
        resp = requests.get(url, params=encoded_payload_dic).json()
        
        response_code = resp["response"]["header"]["resultCode"]
        response_msg = resp["response"]["header"]["resultMsg"]
        
        item_dict = None

        if response_code == "00":
            try:
                item_dict = resp["response"]["body"]["items"]["item"]
            except:
                item_dict = None

        return {"code": response_code, "code_msg" : response_msg, "data": item_dict}
    
    def get_station_exit(self, station_id : str) -> dict[str, str | list[dict[str, str]] | None]:
        url = self.endpoint_url + "/getSubwaySttnExitAcctoBusRouteList?"
        payload_dic = {"serviceKey" : self.service_key, "subwayStationId" : station_id, "pageNo" : self.page_no, "numOfRows" : self.num_of_rows, "_type" : self.return_type}
        
        encoded_payload_dic = urllib.parse.urlencode(payload_dic, safe="%&")
        
        resp = requests.get(url, params=encoded_payload_dic).json()
    

        response_code = resp["response"]["header"]["resultCode"]
        response_msg = resp["response"]["header"]["resultMsg"]
        
        item_dict = None

        if response_code == "00":
            try:
                item_dict = resp["response"]["body"]["items"]["item"]
            except:
                item_dict = None

        return {"code": response_code, "code_msg" : response_msg, "data": item_dict}

    def get_facility_near_station(self, station_id : str) -> dict[str, str | list[dict[str, str]] | None]:
        url = self.endpoint_url + "/getSubwaySttnExitAcctoCfrFcltyList?"
        payload_dic = {"serviceKey" : self.service_key, "subwayStationId" : station_id, "pageNo" : self.page_no, "numOfRows" : self.num_of_rows, "_type" : self.return_type}
        
        encoded_payload_dic = urllib.parse.urlencode(payload_dic, safe="%&")
        
        resp = requests.get(url, params=encoded_payload_dic).json()
    

        response_code = resp["response"]["header"]["resultCode"]
        response_msg = resp["response"]["header"]["resultMsg"]
        
        item_dict = None

        if response_code == "00":
            try:
                item_dict = resp["response"]["body"]["items"]["item"]
            except:
                item_dict = None

        return {"code": response_code, "code_msg" : response_msg, "data": item_dict}
    
    def get_schudule_by_station(self, station_id : str, daily_type_code : Literal['01', '02', '03'], up_down_type_code : Literal['U', 'D']) -> dict[str, str | list[dict[str, str]] | None]:
        url = self.endpoint_url + "/getSubwaySttnAcctoSchdulList?"
        payload_dic = {"serviceKey" : self.service_key, "dailyTypeCode" : daily_type_code, "upDownTypeCode" : up_down_type_code, "subwayStationId" : station_id, "pageNo" : self.page_no, "numOfRows" : self.num_of_rows, "_type" : self.return_type}
        
        encoded_payload_dic = urllib.parse.urlencode(payload_dic, safe="%&")
        
        resp = requests.get(url, params=encoded_payload_dic).json()
    
        
        response_code = resp["response"]["header"]["resultCode"]
        response_msg = resp["response"]["header"]["resultMsg"]
        
        item_dict = None

        if response_code == "00":
            try:
                item_dict = resp["response"]["body"]["items"]["item"]
            except:
                item_dict = None

        return {"code": response_code, "code_msg" : response_msg, "data": item_dict}


