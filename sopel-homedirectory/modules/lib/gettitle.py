from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display

import urllib3.exceptions

import traceback
import string
import time
import re

printable = set(string.printable)

class Titler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.display = Display(visible=0, size=(1920, 1080))
        self.display.start()
        options.add_argument('window-size=1200x600')

        self.driver = webdriver.Chrome(options = options)
        self.driver.implicitly_wait(5)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()
        if self.display:
            self.display.stop()

    def GetTitle(self, url):
        url = ''.join(filter(lambda x: x in printable, url))
        title = False
        try:
            self.driver.get(url)
#            WebDriverWait(self.driver, 10).until(
#                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
#            )
            time.sleep(1)
            if 'twitter.com' in url:
                time.sleep(3)
            title = WebDriverWait(self.driver, 10).until(
                    TitleContainsText()
            )
        except urllib3.exceptions.HTTPError:
            pass
        except Exception as exc:
            print(traceback.format_exc())
            print(exc)
        return title


class TitleContainsText(object):
    def __call__(self, driver):
        title = driver.title
        if re.match(r'[\S]+', title) is not None:
            return title
        else:
            return False


if __name__ == '__main__':
    with Titler() as titler:
        t = titler.GetTitle('https://google.com')
        print(t)
        t = titler.GetTitle('http://bcfhkdlnmvrstwzx.neverssl.com/online')
        print(t)
        t = titler.GetTitle('https://www.nytimes.com/2019/10/31/us/keystone-pipeline-leak.html')
        print(t)
        t = titler.GetTitle('https://www.washingtonpost.com/world/asia_pacific/chinese-official-to-us-after-limits-put-on-its-journalists-lets-play/2020/03/03/fed674d8-5d34-11ea-ac50-18701e14e06d_story.html')
        print(t)
        t = titler.GetTitle('https://twitter.com/TessaDuvall/status/1234960398631219200')
        print(t)
        print('OK')

