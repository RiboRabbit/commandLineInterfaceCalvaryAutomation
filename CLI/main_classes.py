import re
import requests
from bs4 import BeautifulSoup
import links_payloads as lp

class GetDataBs4():

    def __init__(self) -> None:
        self.soup = BeautifulSoup


    def get_spnr_pay_details_from_content(self,content,parser='html.parser'):
        out = {}
        
        s = self.soup(content,features=parser)
        history_table = s.find("div", { "id" : "History_body" })
        table_rows = history_table.findAll("tr")
        for row in table_rows:
            for data in row.findAll("td"):
                if type(data) == "str":
                    print(" ".join(data.findAll(text=True).strip()))
                    pass
                else:
                    for tag in data.findAll('a',href=True):
                        print(tag)
                        print(tag.string)
        # print("------------End--------------")
        # print(type(history_table))
        # try:
        #     amt_rows = history_table.findAll('tr')
        #     if amt_rows != None:
        #         for amt_row in amt_rows:
        #             result = {}

        #             cells = amt_row.findAll('td')

        #             result["sno"]             = " ".join(cells[0].findAll(text=True)).strip()
        #             result["p_date"]          =  " ".join(cells[1].findAll(text=True)).strip()
        #             result["rec_code"]        =  " ".join(cells[2].findAll(text=True)).strip()
        #             result["rec_code_url"]    =  f"http://202.153.33.67/" + cells[2].findAll(href=True)
        #             result["rec_no"]          =  " ".join(cells[3].findAll(text=True)).strip()
        #             result["p_status"]        =  " ".join(cells[4].findAll(text=True)).strip()
        #             result["pay_mode"]        =  " ".join(cells[5].findAll(text=True)).strip()
        #             result["pay_location"]    =  " ".join(cells[6].findAll(text=True)).strip()
        #             result["tv_ch"]           =  " ".join(cells[7].findAll(text=True)).strip()
        #             result["remarks"]         =  " ".join(cells[8].findAll(text=True)).strip()
        #             result["p_amount"]        =  " ".join(cells[9].findAll(text=True)).strip()
        #             result["edit_url"]        =  f"http://202.153.33.67/"+ cells[10].findAll(href=True)[0]['href']
        #             out[counter] = result
        # except AttributeError as e:
        #     print(e)
        
        return out

    def get_numbers(self,str):
        array = re.findall(r'[0-9]+', str)
        return " ".join(array)


    def extract_table_data(self,content,parser="html.parser"):
        out = []
        s = self.soup(content,features=parser)
        table = s.find("table","table")
        try:
            table_values = table.findAll("tr")
            if table_values != None:
                
                for row in table_values:
                    result = {}
                    cells = row.findAll('td')
                    if len(cells) == 6:
                        result["sno"]       = " ".join(cells[0].findAll(text=True)).strip()
                        result["scode"]     = " ".join(cells[1].findAll(text=True)).strip()
                        result["sname"]     = " ".join(cells[2].findAll(text=True)).strip()
                        result["snumber"]   = " ".join(cells[3].findAll(text=True)).strip()
                        result["slocation"] = " ".join(cells[4].findAll(text=True)).strip()
                            # Getting ID for adding receipt
                        ID = cells[5].findAll(href=True)[0]["href"]
                        ID = self.get_numbers(ID)   
                        result["sid"]       = ID
                        out.append(result)
        except AttributeError as e:
            print(e)
        
        return out


class NoSponsorFoundException(Exception):
    pass        

class CalvarySession():


    def __init__(self):
        self.s = requests.Session()
        self.login()
        self.recent_search = []

    def login(self):
        return self.s.post(lp.login_url,data=lp.login_url_payload,headers=lp.headers)

    

    def search_keyword(self, keyword):

        """
            Input : Enter KeyWord to search
            Exception: may raise NoSponsorFoundException
            output : Index form recent Search

        """

        response = self.s.post(lp.get_new_sponsors_url,data=lp.get_new_sponsors_payload(keyword),headers=lp.headers)
        
        self.recent_search = GetDataBs4().extract_table_data(content=response.content)
        
        if len(self.recent_search) == 0:
            raise NoSponsorFoundException("No Sponsor avaliable with that keyword")

        for index,user in enumerate(self.recent_search):
            keyword = keyword.upper()
            if user["snumber"] == keyword:
                return (True,index)

            if user["sname"] == keyword:
                return (True,index)
            
            if user["scode"] == keyword:
                return (True,index)

        return None

    def __del__(self):
        self.s.close()

    def submit_receipt(self):
        pass

    def get_sponsor(self,keyword):

        """
            input : Keyword used to search
            Exception: raises NoSponsorFoundException
            output : Json Object of Sponsor Details
        """

        try:

            is_present = self.search_keyword(keyword)
            if is_present[0] == True:
                return self.recent_search[is_present[1]]
            else:
                raise NoSponsorFoundException("Data Not Found")
        except NoSponsorFoundException as e:
            raise

    def get_spnr_details_as_json(self,rec_id):
        raw_data = self.s.post(lp.add_receipt_data_url,data=lp.add_receipt_data_payload(rec_id=rec_id),headers=lp.headers)
        data_from_response = GetDataBs4().get_spnr_pay_details_from_content(content=raw_data.content)
        return data_from_response

    def get_sponsors_full_details(self,keyword):
        
        spnr = self.get_sponsor(keyword=keyword)

        print(self.get_spnr_details_as_json(spnr["sid"]))
        



    