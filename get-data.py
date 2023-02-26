from bs4 import BeautifulSoup
import requests
import dotenv
import os
import time
import pandas as pd
import csv


class Scrape():
    def __init__(self):
        self.__url = 'https://9anime.to/user/watch-list'
        self.__soup = None
        self.__numOfPages = 6
        dotenv.load_dotenv('secret.env')
        self.__cookies = {
            "session": os.environ.get('SESS')
        }
        self.__list = {}
        self._query = 'folder='
        self.pageNameCases = {
            1: 'Watching',
            2: 'Watched',
            3: 'On-Hold',
            4: 'Dropped',
            5: 'Planned'
        }

    def getSoupFolder(self, n):
        newquery = self._query + str(n)
        newUrl = self.__url + f'?{newquery}'
        print(newUrl)
        r = requests.get(newUrl, cookies=self.__cookies)
        s = BeautifulSoup(r.text, 'html.parser')
        return s

    def getSoupPage(self, n, i):
        newquery = self._query + f'{str(n)}&page={str(i)}'
        newUrl = self.__url + newquery
        print(newUrl)
        r = requests.get(newUrl, cookies=self.__cookies)
        s = BeautifulSoup(r.text, 'html.parser')
        return s

    def getSoupData(self):
        for n in range(1, self.__numOfPages):
            animeNList = []
            s = self.getSoupFolder(n)
            listOfAnimeNamestag = s.find_all(class_='d-title')
            animeNList = [n.text for n in listOfAnimeNamestag]
            for i in range(2, 20):
                s = self.getSoupPage(n, i)
                listOfAnimeNamestag = s.find_all(class_='d-title')
                # print(listOfAnimeNamestag)
                if len(listOfAnimeNamestag) != 0:
                    animeNList = animeNList + \
                        ([n.text for n in listOfAnimeNamestag])
                else:
                    break
            print(self.pageNameCases[n])
            print(animeNList)
            self.__list[self.pageNameCases[n]] = animeNList
        print(self.__list)
        # for n in range(1, 2):
        #     query = self._query + str(n)
        #     url = self.__url + f"?{query}"
        #     print(url)
        #     r = requests.get(url, cookies=self.__cookies)
        #     s = BeautifulSoup(r.text, 'html.parser')
        #     # s = self.getSoupFolder(n)
        #     with open('soup.html', 'w+', encoding='utf-8') as f:
        #         f.write(str(s.prettify()))
        #         f.close()
        #     AnimeNameHtmlTag = s.find_all(class_='d-title')
        #     animeNList = [n.text for n in AnimeNameHtmlTag]
        #     time.sleep(2)
        #     print(animeNList)
        #     print(len(animeNList))

    def saveData(self):
        # animeNamedf = pd.DataFrame.from_dict(self.__list)
        # print(animeNamedf)
        # animeNamedf.to_csv('Anime.csv', sep='\t', encoding='utf-8')
        # print('data saved to csv')
        l = []
        with open('Anime.csv', 'w', encoding='utf-8') as f:
            w = csv.DictWriter(f, self.__list.keys())
            w.writeheader()
            w.writerows(self.__list)


if __name__ == '__main__':
    s = Scrape()
    s.getSoupData()
    s.saveData()

    # cookies = {
    #     "session": 'xdk6BLMZSnOW6r7X1BbGEUDNBn2XX2glbjMiO5HI'
    # }
    # req = requests.get('https://9anime.to/user/watch-list?folder=1', cookies=cookies)
    # s = BeautifulSoup(req.text, 'html.parser')
    # all = s.find_all(class_ = 'd-title')
    # l = [n.text for n in all]
    # print(l)
    # print(len(l))
    # print('scrape')
    # with open('soup.html', 'w', encoding='utf-8') as f:
    #     f.write(str(s.prettify()))
    #     f.close()