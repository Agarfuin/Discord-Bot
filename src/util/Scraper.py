from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, address):
        self.__address = address
        self.__codes = self.scrap_codes()
    
    def get_address(self):
        return self.__address
    
    def set_address(self, address):
        self.__address = address
        
    def get_codes(self):
        return self.__codes
    
    def set_codes(self, codes):
        self.__codes = codes
    
    def print_codes(self):
        codes = self.get_codes()
        final_code = ""
        for code in codes:
            final_code += f"[{code}](<https://genshin.hoyoverse.com/en/gift?code={code}>)\n"
        return final_code
    
    def scrap_codes(self):
        list_codes = []
        page = requests.get(self.get_address())
        soup = BeautifulSoup(page.content, "html.parser")
        list(soup.children)
        codes = soup.find_all('code')
        for i in range(5):
            list_codes.append(codes[i].get_text())
        return list_codes
    
    def update_codes(self):
        current_codes = self.get_codes()
        new_codes = self.scrap_codes()
        if len(new_codes) == len(current_codes) and len(new_codes) == sum([1 for i, j in zip(new_codes, current_codes) if i == j]):
            return 0
        else:
            set1 = set(current_codes)
            set2 = set(new_codes)
            new_codes = list(set2 - set1)
            self.set_codes(new_codes)
            return 1
        
        
        
        
        