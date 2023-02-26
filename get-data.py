from bs4 import BeautifulSoup
import requests
import dotenv
import os

# class Scrape():
#     def __init__(self):
#         self.__url = 'https://9anime.to/home'
#         self._soup = None
    
#     def getSoup(self):
#         payload = {
#             'username':'cyrof',
#             'password':'B@sketba1l'
#         }
#         cookies = {
#             'session' : 'V3WWFmraoxSJVu2kvbhtQxlqEorvKMuNhxNdi1iR'
#         }
#         with requests.Session() as s:
#             req = s.post('https://9anime.to/ajax/user/login', data=payload, cookies=cookies)
#             print(req.text)

#             r = s.get('https://9anime.to/user/watch-list')
#             print(r.text)

# if __name__ == '__main__':
#     s = Scrape()
#     s.getSoup()
# cookie = {
#     'session' : 'V3WWFmraoxSJVu2kvbhtQxlqEorvKMuNhxNdi1iR'
# }
# req = requests.get('https://9anime.to/user/watch-list', cookies=cookie)
# print(req.text)

class Scrape():
    def __init__(self):
        self.__url = 'https://9anime.to/user/watch-list'
        self.__soup = None
        self.__numOfPages = 5
        self.__cookies = {
            "session": None
        }
        dotenv.load_dotenv('secrets.env')
        self.__sess = os.environ.get('SESS')
    
    def getSoupForPages(self):
        self._query = 'folder'
        self.pageName = {
            1 : 'Watching',
            2 : 'Watched',
            3 : 'On-Hold',
            4 : 'Dropped',
            5 : 'Planned'
        }

        self._query = self._query + str(1)
        r = requests.get(self.__url + f'?{self._query}', cookies=self.__cookies)
        self.__soup = BeautifulSoup(r.text, 'html.parser')
        
        # for n in self.__numOfPages:
        #     self._query = self._query + str(n)
        #     r = requests.get(self.__url + f'?{self._query}', cookies=self.__cookies)

    

