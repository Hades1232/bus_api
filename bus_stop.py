import requests
import urllib.parse
import json
from typing import Literal
import city_code

with open("key.json", "r") as f:
    data = json.load(f)

SERVICE_KEY = data["api_key"]



class BusStop(city_code.CityCode):

    def __init__(self, page_no : str = "1", num_of_rows : str = "10", return_type : Literal["json", "xml"] = "json") -> None:
        self.endpoint_url = "http://apis.data.go.kr/1613000/BusSttnInfoInqireService"
        self.service_key = SERVICE_KEY
        self.page_no = page_no
        self.num_of_rows = num_of_rows
        self.return_type = return_type

        super().__init__(self.endpoint_url)

        
    def get_bus_stop_info(self, stop_name : str, city_code: str, stop_num : str = None) -> dict[str, str | list[dict[str, str]], None]:
        
        url = self.endpoint_url + "/getSttnNoList?"
        payload_dic = {"serviceKey" : self.service_key, "nodeNm": stop_name, "stop_num" : stop_num, "cityCode" : city_code, "pageNo" : self.page_no, "numOfRows" :self.num_of_rows, "_type" : self.return_type}
        encoded_payload_dic = urllib.parse.urlencode(payload_dic, safe="%&")

        resp = requests.get(url, params=encoded_payload_dic).json()
        print(resp)

        response_code = resp["response"]["header"]["resultCode"]
        response_msg = resp["response"]["header"]["resultMsg"]
        
        item_dict = None

        if response_code == "00":
            try:
                item_dict = resp["response"]["body"]["items"]["item"]
            except:
                item_dict = None

        return {"code": response_code, "code_msg" : response_msg, "data": item_dict}

    def get_bus_stop_by_gps(self, gps_lati : str, gps_long : str, city_code: str) -> dict[str, str | list[dict[str, str]] | None]:
        
        url = self.endpoint_url + "/getCrdntPrxmtSttnList?"
        payload_dic = {"serviceKey" : self.service_key, "gpsLati": gps_lati, "gpsLong" : gps_long, "cityCode" : city_code, "pageNo" : self.page_no, "numOfRows" :self.num_of_rows, "_type" : self.return_type}
        encoded_payload_dic = urllib.parse.urlencode(payload_dic, safe="%&")

        resp = requests.get(url, params=encoded_payload_dic).json()
        print(resp)

        response_code = resp["response"]["header"]["resultCode"]
        response_msg = resp["response"]["header"]["resultMsg"]
        
        item_dict = None

        if response_code == "00":
            try:
                item_dict = resp["response"]["body"]["items"]["item"]
            except:
                item_dict = None

        return {"code": response_code, "code_msg" : response_msg, "data": item_dict}

    def get_route_by_stop_id(self, stop_id : str, city_code: str) -> dict[str, str | list[dict[str, str]] | None]:
        
        url = self.endpoint_url + "/getSttnThrghRouteList?"
        payload_dic = {"serviceKey" : self.service_key, "nodeid": stop_id, "cityCode" : city_code, "pageNo" : self.page_no, "numOfRows" :self.num_of_rows, "_type" : self.return_type}
        encoded_payload_dic = urllib.parse.urlencode(payload_dic, safe="%&")

        resp = requests.get(url, params=encoded_payload_dic).json()
        print(resp)

        response_code = resp["response"]["header"]["resultCode"]
        response_msg = resp["response"]["header"]["resultMsg"]
        
        item_dict = None

        if response_code == "00":
            try:
                item_dict = resp["response"]["body"]["items"]["item"]
            except:
                item_dict = None

        return {"code": response_code, "code_msg" : response_msg, "data": item_dict}
