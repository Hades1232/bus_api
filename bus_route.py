import requests
import urllib.parse
import city_code
from typing import Optional, List, Dict, Union, Literal
import folium
import json



with open("key.json", "r") as f:
    data = json.load(f)

SERVICE_KEY = data["api_key"]


class BusRoute(city_code.CityCode):
    def __init__(self, page_no : str = "1", num_of_rows : str = "10", return_type : Literal["json", "xml"] = "json") -> None:

        self.endpoint_url = "https://apis.data.go.kr/1613000/BusRouteInfoInqireService"
        self.service_key = SERVICE_KEY
        self.page_no = page_no
        self.num_of_rows = num_of_rows
        self.return_type = return_type

        
        super().__init__(self.endpoint_url)

    def get_route_num_list(self, bus_number : str, city_code : str) -> Dict[str, Union[str, List[dict[str, str]], None]]:
        url = self.endpoint_url + "/getRouteNoList?"
        payload_dic = {"serviceKey" : self.service_key, "routeNo": bus_number, "cityCode" : city_code, "pageNo" : self.page_no, "numOfRows" :self.num_of_rows, "_type" : self.return_type}
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


    def get_all_buses_list(self, city_code : str) -> List[str]:
        
        saved_num_of_rows = self.num_of_rows

        self.num_of_rows = "300"
        routes_num_list = self.get_route_num_list("", city_code)["data"]
        self.num_of_rows = saved_num_of_rows
        
        buses_list = list(m['routeno'] for m in routes_num_list)
       
        sorted_buses_list = sorted(list(set(buses_list)), key=str)
        
        return list(map(str, sorted_buses_list))


    def get_route_stop(self, city_code : str, route_id : str) -> Dict[str, Union[str, List[dict[str, str]], None]]:
        url = self.endpoint_url + "/getRouteAcctoThrghSttnList?"
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

    def get_route_info(self, city_code : str, route_id : str) -> Dict[str, Union[str, List[dict[str, str]], None]]:
        url = self.endpoint_url + "/getRouteInfoIem?"
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

    def generate_html_file_TEST(e : dict):
        mid_x = e["data"][len(e["data"]) // 2]["gpslati"]
        mid_y = e["data"][len(e["data"]) // 2]["gpslong"]
        
        maps = folium.Map(
            location=[mid_x,mid_y], 
            zoom_start=20, 
            tiles="http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}",
            attr="Google Maps"
        )


        for i in e["data"]:
            x = i["gpslati"]
            y = i["gpslong"]
            stop_name = i["nodenm"]
            folium.Marker(
            location=[x,y],
            popup=stop_name,
            tooltip=f"{stop_name} 정류장",
            icon=folium.Icon(color='lightgreen',icon='bus', prefix="fa")
            ).add_to(maps)

            maps.save('map.html')    






