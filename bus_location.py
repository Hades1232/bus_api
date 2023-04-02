import requests
import urllib
from typing import Literal
import city_code

import json
import bus_route


with open("key.json", "r") as f:
    data = json.load(f)

SERVICE_KEY = data["api_key"]


class BusLocation(city_code.CityCode):
    
    def __init__(self, page_no : str = "1", num_of_rows : str = "10", return_type : Literal["json", "xml"] = "json") -> None:
        self.endpoint_url = "https://apis.data.go.kr/1613000/BusLcInfoInqireService"
        self.service_key = SERVICE_KEY
        self.page_no = page_no
        self.num_of_rows = num_of_rows
        self.return_type = return_type

        super().__init__(self.endpoint_url)

    def get_bus_location_by_route(self, city_code: str, route_id : str) -> dict[str, str | list[dict[str, str]] | None]:
        url = self.endpoint_url + "/getRouteAcctoBusLcList?"
        payload_dic = {"serviceKey" : self.service_key, "routeId": route_id, "cityCode" : city_code, "pageNo" : self.page_no, "numOfRows" :self.num_of_rows, "_type" : self.return_type}
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

    def get_bus_location_by_stop(self, city_code: str, route_id: str, stop_id: str) -> dict[str, str | list[dict[str, str]] | None]:
        url = self.endpoint_url + "/getRouteAcctoSpcifySttnAccesBusLcInfo"
        payload_dic = {"serviceKey" : self.service_key, "routeId": route_id, "nodeId" : stop_id, "cityCode" : city_code, "pageNo" : self.page_no, "numOfRows" :self.num_of_rows, "_type" : self.return_type}
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


