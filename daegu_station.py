import requests
import json
from typing import Literal


with open("key.json", "r") as f:
    data = json.load(f)

SERVICE_KEY = data["decoded_api_key"]

class DaeguStation:

    def __init__(self, page : str = "1", per_page : str = "10", return_type : Literal["json", "xml"] = "json") -> None:
        self.endpoint_url = "https://api.odcloud.kr/api"
        self.service_key = SERVICE_KEY
        self.page = page
        self.per_page = per_page
        self.return_type = return_type
        self.headers = {'Authorization' : f"Infuser {SERVICE_KEY}"}
        self.line_numbers = {'1' : '1호선', '2' : '2호선', '3' : '3호선'}

        
    def get_station_transfer_info(self, line_num : Literal['1', '2', '3'] = None) -> dict[str, str | list[dict[str, str]] | None]:
        url = self.endpoint_url + "/15041092/v1/uddi:2e032952-4deb-4198-a6c2-e9d6bcf6eab5?"
        payload_dic = {"page" : self.page, "perPage" : self.per_page, "returnType" : self.return_type}
        
        #encoded_payload_dic = urllib.parse.urlencode(payload_dic)

        resp = requests.get(url, params=payload_dic, headers=self.headers)
        

        response_code = resp.status_code
        
        item_dict = None

    
        if response_code == 200:
            try:
                item_dict = resp.json()["data"]
            except:
                item_dict = None

        if line_num != None and item_dict != None:
            line_name = self.line_numbers[line_num]
            item_dict = list(filter(lambda i: i['선명'] == line_name, item_dict))
            
            

        return {"code": response_code, "data": item_dict}
    

