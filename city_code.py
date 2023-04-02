import requests
import urllib.parse



class CityCode:
    def __init__(self, endpoint_url : str, return_type : str = "json") -> None:
        self.endpoint_url = endpoint_url
        self.return_type = return_type

    def get_city_code_list(self) -> dict[str, str | list[dict[str, str]] | None]:
        url = self.endpoint_url + "/getCtyCodeList?"
        payload_dic = {"serviceKey" : self.service_key, "_type" : self.return_type}
        encoded_payload_dic = urllib.parse.urlencode(payload_dic, safe="%&")     
        resp = requests.get(url = url, params=encoded_payload_dic)

        response_code = resp.json()["response"]["header"]["resultCode"]
        response_msg = resp.json()["response"]["header"]["resultMsg"]
        
        item_dict = None

        if response_code == "00":
            item_dict = resp.json()["response"]["body"]["items"]["item"]

        return {"code": response_code, "code_msg" : response_msg, "data": item_dict}

    def get_city_code(self, city_code_list : list[dict], city_name : str) -> str | None:
        city_name_list = list(m['cityname'] for m in city_code_list)
        try:
            city_name_list_index = city_name_list.index(city_name)
        except:
            return None

        return city_code_list[city_name_list_index]["citycode"]
    
