import os
import sys
import getData


def runScrape():
    """
    Run the scraping process. 
    This function initialises the Scapre class, retrieves the data, saves it to a CSV file,
    and converts the CSV file to an Excel file.
    """
    s = getData.Scrape()
    s.getSoupData()
    s.saveData()
    s.convert_excel()


def create_env(sess):
    """
    Create a .env file and write the session ID to it.
    :param sess: the session ID to be written to the .env file
    """
    with open(r'secret.env', 'w') as f:
        f.write(f'SESS={sess}')
        f.close()

def get_sess():
    """
    Prompt the user to log in to aniwave and provide the session ID.
    The session ID is then written to a .env file.
    """
    print('Please manually log into aniwave. Afterwards please copy and paste the session id. session id can be found under cookies in dev console')
    sess = input('Session ID: ')
    create_env(sess=sess)

if sys.platform == 'win32':
    get_sess()
    runScrape()
elif sys.platform == 'linux':
    get_sess()
    runScrape()
