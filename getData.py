from bs4 import BeautifulSoup
import requests
# import dotenv
import os
import time
import pandas as pd
from tqdm import tqdm


class Scrape():
    def __init__(self, cookies=None):
        """
        Initialise the Scrape class.
        """
        self.__url = 'https://aniwavetv.to/user/watch-list'
        self.__numOfFolders = 6 # Number of folders to scrape
        # dotenv.load_dotenv('secret.env') # dotenv is deprecated in Python 3.12.4
        # self.__cookies = {
        #     "session": os.environ.get('SESS') # Session cookie fro authentication
        # }
        self.__cookies = {
            "session": cookies
        }
        self.__list = [] # List to store DataFrames for each folder
        self._query = 'folder=' #   Query string for folder parameter
        self.pageNameCases = {
            1: 'Watching',
            2: 'Watched',
            3: 'On-Hold',
            4: 'Dropped',
            5: 'Planned'
        } # Mapping folder numbers to their name

    def getSoupFolder(self, n):
        """
        Get the BeautifulSoup object for the initial page of a folder
        :param n: folder number
        :return s: returns BeautifulSoup Parsed with HTML of the folder page
        """
        newquery = self._query + str(n)
        newUrl = self.__url + f'?{newquery}'
        # print(newUrl)
        r = requests.get(newUrl, cookies=self.__cookies)
        s = BeautifulSoup(r.text, 'html.parser')
        return s

    def getSoupPage(self, n, i):
        """
        Get the BeautifulSoup object for a specific page of a folder.
        :param n: Folder number
        :param i: Page number
        :return s: return BeautifulSoup with Parsed HTML of the specific page
        """
        MAX_RETRIES = 15
        newquery = self._query + f'{str(n)}&page={str(i)}'
        newUrl = self.__url + f'?{newquery}'
        retry_counter = 0
        print(newUrl)
        while True:
            # print("test")
            # print(self.__cookies)
            r = requests.get(newUrl, cookies=self.__cookies)
            # print(r)
            if r.status_code != 200 and retry_counter <= MAX_RETRIES:
                time.sleep(5) # Wait and retry if the request fails
                print(f"Status code: {r.status_code}. Retrying...")
                continue
            elif retry_counter > MAX_RETRIES:
                print("Program timeout. Retried 15 times.")
                break
            else:
                retry_counter = 0 # reset retry counter
                break
        # print(r)
        s = BeautifulSoup(r.text, 'html.parser')
        return s

    def getSoupData(self):
        """
        Scrape anime data from all folders and store them in the list of DataFrames.
        """
        for n in tqdm(range(1, self.__numOfFolders), desc="Scraping Folders"):
            animeNList = []
            # print(n)
            s = self.getSoupFolder(n)
            listOfAnimeNamestag = s.find_all(class_='d-title')
            animeNList = [n.text for n in listOfAnimeNamestag]
            for i in tqdm(range(1, 20), desc=f"Scraping Pages for Folder {n}", leave=False):
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
        """
        Create a DataFrame from the list of anime names for a specific folder.
        :param ListOfAnimeNames: list of anime names
        :param n: folder number 
        :return df: return the DataFrame containing the anime names
        """
        df = pd.DataFrame(listOfAnimeNames, columns=[self.pageNameCases[n]])
        return df


    def saveData(self):
        """
        Save the scraped data to a CSV file.
        """
        df_concat = pd.concat(self.__list, axis=1)
        df_concat.to_csv('Anime.csv', encoding='utf-8')
        print("Saved to csv file")

    def convert_excel(self):
        """
        Convert the CSV file to an Excel file
        """
        csvData = pd.read_csv('Anime.csv', encoding='utf-8')
        excelFile = pd.ExcelWriter('ListOfAnime.xlsx')
        csvData.to_excel(excelFile, index=False)
        excelFile.close()
        print("Saved to excel file")
        
if __name__ == '__main__':
    s = Scrape()
    s.getSoupData()
    s.saveData()
    s.convert_excel()