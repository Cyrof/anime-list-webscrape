# Anime Watch List Scraper (Archived)
### Note: This project has been archived due to the recent closure of the Aniwave website and its clone sites.

This project is a web scraper designed to collect data from the user's watch list on the Aniwave website (or its clones). The scraped data includes anime titles organised by different folder categories such as Watching, Watched, On-Hold, Dropped, and Planned. The data is saved to a CSV file and then converted to an Excel file for easy viewing and mangement.

## Requirements

- Python 3.10
- BeautifulSoup
- Requests
- Python-dotenv
- Pandas

## Installation

1. **Clone the Repository:**
    ```bash
    $ git clone https://github.com/Cyrof/anime-list-webscrape.git
    $ cd anime-list-webscrape
    ```
2. **Install the required packages:**
    ```bash
    $ pip install -r requirements.txt
    ```

## Configuration

Before running the scraper, you need to configure it according to your specific setup on Aniwave (or its clones).

1. **Update Number of Folders**
    In `getData.py`, update the `self.__numOfFolder` variable on line 15 to reflect the number of folders you have on your watch list. Do not include the "All" folder.
    
    ```python
    self.__numOfFolders = 6 # Update this number according to your folders
    ```

2. **Update Folder Names**
    In `getData.py`, update the `self.pageNameCases` dictionary on line 22 to map folder numbers to their corresponding names. Ensure this mapping corresponds to your folder names on the website.

    ```python
    self.pageNameCases = {
        1: 'Watching',
        2: 'Watched',
        3: 'On-Hold',
        4: 'Dropped',
        5: 'Planned'
        # Update these names according to your folders
    }
    ```

3. **Update Website URL**
    Due to the instability of the Aniwave website, multiple clone sites exist. Update the `self.__url` variable on line 14 in `getData.py` to reflect the URL of the site you are using.

    ```python
    self.__url = 'https://aniwavetv.to/user/watch-list' # Update with the current website link
    ```

4. **Update Headers**
   In `run.py`, there is a `headers` variable that may need to be updated. To do this, navigate to the Network tab in Developer Tools and get the header from a request to the Aniwave website. Update the `headers` variable with these values.

   ```python 
   headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0"
   }
   ```

## Retrieve Session ID
1. Log into your Aniwave account.
2. Open Developer Tools: 
    - Right-click on the webpage and select `Inspect`, or press `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Opt+T` (Mac).
3. Navigate to the Application tab: 
    - Click on the `Application` tab in the Developer Tools window.  <br /> <br />
    ![Application tab](https://github.com/Cyrof/anime-list-webscrape/blob/master/Images/app_tab.png)

4. Find the Session ID:
    - Under the `Storage` section in the left-hand sidebar, click on `Cookies` and then select the Aniwave website URL.  <br /> <br />
    ![Cookies](https://github.com/Cyrof/anime-list-webscrape/blob/master/Images/cookie_tab.png)

    - In the right-hand panel, look for a key called `session`. The value corresponding to this key is your session ID.  <br /> <br />
    ![session key](https://github.com/Cyrof/anime-list-webscrape/blob/master/Images/sess_key.png)

## Usage

1. **Run the scraper:**
    ```sh
    python run.py
    ```

2. **Input your session ID:**
    The program well prompt you to log into the Aniwave website manually and copy the session ID from your browser's developer console. Paste the session ID when prompted.

## Output

The scraped data will be saved as `Anime.csv` and `ListOfAnime.xlsx` in the project directory.

## Notes

- The scraper includes mechanisms to handle the unstable nature of the Aniwave website by retrying requests if they fail.

- Ensure you have a stable internet connection during the scraping process.

- This project assumes a specific structure and naming convention for the folders on the Aniwave website. Adjust the configuration accordingly if your setup differs.

## License

This project is licensed under the MIT license. See the [`License`](https://github.com/Cyrof/anime-list-webscrape/blob/master/LICENSE) file for details.

## Archival Notice
Due to the recent closure of the Aniwave website and its clones, this project is no longer functional and has been archived. 

Thank you for your interest and support!