from bs4 import BeautifulSoup
import requests
import dotenv
import os
import time
import pandas as pd


class Scrape():
    def __init__(self):
        self.__url = 'https://aniwave.bz/user/watch-list'
        self.__numOfFolders = 6
        dotenv.load_dotenv('secret.env')
        self.__cookies = {
            "session": os.environ.get('SESS')
        }
        self.__list = []
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
        newUrl = self.__url + f'?{newquery}'
        print(newUrl)
        while True:
            print("test")
            print(self.__cookies)
            r = requests.get(newUrl, cookies=self.__cookies)
            print(r)
            if r.status_code != 200:
                time.sleep(5)
                continue
            else:
                break
        print(r)
        s = BeautifulSoup(r.text, 'html.parser')
        return s

    def getSoupData(self):
        for n in range(1, self.__numOfFolders):
            animeNList = []
            print(n)
            s = self.getSoupFolder(n)
            listOfAnimeNamestag = s.find_all(class_='d-title')
            animeNList = [n.text for n in listOfAnimeNamestag]
            for i in range(2, 20):
                s = self.getSoupPage(n, i)
                # print(s)
                listOfAnimeNamestag = s.find_all(class_='d-title')

                if len(listOfAnimeNamestag) != 0:
                    animeNList = animeNList + \
                        ([n.text for n in listOfAnimeNamestag])
                    time.sleep(5)
                else:
                    break

            self.__list.append(self.createDF(animeNList, n=n))
            time.sleep(1)


    def createDF(self, listOfAnimeNames, n):
        df = pd.DataFrame(listOfAnimeNames, columns=[self.pageNameCases[n]])
        return df


    def saveData(self):
        df_concat = pd.concat(self.__list, axis=1)
        df_concat.to_csv('Anime.csv', encoding='utf-8')

    def convert_excel(self):
        csvData = pd.read_csv('Anime.csv', encoding='utf-8')
        excelFile = pd.ExcelWriter('ListOfAnime.xlsx')
        csvData.to_excel(excelFile, index=False)
        excelFile.save()
        
if __name__ == '__main__':
    s = Scrape()
    s.getSoupData()
    s.saveData()
    s.convert_excel()