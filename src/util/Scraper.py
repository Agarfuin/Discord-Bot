from bs4 import BeautifulSoup
import urllib.request

class Scraper:
    def __init__(self, address):
        self.__address = address
        self.__codes = self.scrap_codes()
    
    def get_address(self):
        return self.__address
    
    def set_address(self, address):
        self.__address = address
        
    def get_all_codes(self):
        return self.__codes
    
    def set_codes(self, codes):
        self.__codes = codes
    
    def get_codes(self):
        ret_list = []
        for i in range(5):
            ret_list.append(self.__codes[i])
        return ret_list
    
    def scrap_codes(self):
        try:
            list_codes = []
            text = urllib.request.urlopen(self.get_address()).read()
            soup = BeautifulSoup(text, 'html.parser')
            list(soup.children)
            codes = soup.find_all('code')
            for code in codes:
                list_codes.append(code.get_text())
            return list_codes
        except Exception as e:
            print(f"Error: {e}")
    
    def update_codes(self):
        current_codes = self.get_all_codes()
        updated_codes = self.scrap_codes()
        if len(updated_codes) == len(current_codes) and len(updated_codes) == sum([1 for i, j in zip(updated_codes, current_codes) if i == j]):
            return None
        else:
            set1 = set(current_codes)
            set2 = set(updated_codes)
            new_codes = list(set2 - set1)
            self.set_codes(updated_codes)
            return new_codes
        
        
        
        
        