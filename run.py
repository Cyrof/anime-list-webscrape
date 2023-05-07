import os
import sys
import getData


def runScrape():
    s = getData.Scrape()
    s.getSoupData()
    s.saveData()
    s.convert_excel()

# create and write env
def create_env(sess):
    with open(r'secret.env', 'w') as f:
        f.write(f'SESS={sess}')
        f.close()

def get_sess():
    print('Please manually log into 9anime.to. Afterwards please copy and paste the session id. session id can be found under cookies in dev console')
    sess = input('Session ID: ')
    create_env(sess=sess)

if sys.platform == 'win32':
    get_sess()
    runScrape()
elif sys.platform == 'linux':
    get_sess()
    runScrape()
