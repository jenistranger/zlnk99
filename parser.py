import time
from datetime import datetime
import random
import json
import fake_useragent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class ParserLolzChrome:
    def __init__(self, state = True) -> None:
        self.__ua  = fake_useragent.UserAgent()
        self.__option = webdriver.ChromeOptions()
        self.__option.add_argument(f"user-agent={self.__ua.random}")
        self.__option.add_argument("--disable-blink-features=AutomationControlled")
        self.__option.add_argument("--disable-notifications")
        self.__srv = ChromeService(ChromeDriverManager().install())
        self.__option.headless = state
            #создание объекта браузер
        self.__browser = webdriver.Chrome(
            service=self.__srv,
            options=self.__option
            )

    #True или False
    def browserMode(self, state):
        self.__option.headless = state

    def getFirstPage(self) -> str:
        time.sleep(2)
        self.__browser.get("https://zelenka.guru/forums/contests/?order=post_date&direction=desc&prefix_id[]=131")
        time.sleep(3)
        lister = self.__browser.find_element(By.CLASS_NAME, "latestThreads").find_elements(By.CLASS_NAME, "discussionListItem")
        data = {}
        now = datetime.now()
        data["lastupd"] = str(now.strftime("%H:%M:%S"))
        data['thread'] = []
        for subj in lister:
            data['thread'].append(
                {
                    #'threadNum' : subj.find_element(By.CLASS_NAME, "listBlock ").get_attribute("href"),
                    'id' : subj.find_element(By.CLASS_NAME, "main ").get_attribute("href")[29:][:-1],
                    'title': subj.find_element(By.CLASS_NAME, "spanTitle").text,
                    'creator' : subj.find_element(By.CLASS_NAME, "username").text,
                    'money' : subj.find_element(By.CLASS_NAME, "moneyContestWithValue").text
                }
            )
        with open("threadsdata/data.json", "w") as inf:
            json.dump(data, inf, ensure_ascii=False, indent=4)

    def getAllPages(self):
        file = open("threadsdata/data.json", "w")
        file.close()
        data = {}
        now = datetime.now()
        #url выводит только розыгрыши с тегом "Деньги"
        self.__browser.get("https://zelenka.guru/forums/contests/?order=post_date&direction=desc&prefix_id[]=131")
        time.sleep(random.randint(1, 3))
        last_data = int(self.__browser.find_element(By.CLASS_NAME, "PageNav").get_attribute("data-last"))
        data["thread"] = []
        listofthreads = self.__browser.find_element(By.CLASS_NAME, "latestThreads").find_elements(By.CLASS_NAME, "discussionListItem")
        for subj in listofthreads:
            data["thread"].append(
                {
                    'id' : subj.find_element(By.CLASS_NAME, "main").get_attribute("href")[29:][:-1],
                    'title': subj.find_element(By.CLASS_NAME, "spanTitle").text,
                    'creator' : subj.find_element(By.CLASS_NAME, "username").text,
                    'money' : subj.find_element(By.CLASS_NAME, "moneyContestWithValue").text
                }
            )
        for page in range(2, last_data+1):
            #data["thread"].clear()
            self.__browser.get(f"https://zelenka.guru/forums/contests/page-{page}?prefix_id[0]=131&enabled=1&createTabButton=1")
            listofthreads = self.__browser.find_element(By.CLASS_NAME, "latestThreads").find_elements(By.CLASS_NAME, "discussionListItem")
            for threadx  in listofthreads:
                moneystr = str(threadx.find_element(By.CLASS_NAME, "moneyContestWithValue").text)
                moneyfoo = lambda money : money if " " not in money else money.replace(" ", "")
                moneyres = moneyfoo(moneystr)
                data["thread"].append(
                    {
                        'id' : threadx.find_element(By.CLASS_NAME, "main").get_attribute("href")[29:][:-1],
                        'title': threadx.find_element(By.CLASS_NAME, "spanTitle").text,
                        'creator' : threadx.find_element(By.CLASS_NAME, "username").text,
                        'money' : moneyres
                    }
                )
        data["lastupd"] = str(now.strftime("%H:%M:%S"))
        with open("threadsdata/data.json", "w") as inf:
            json.dump(data, inf, indent=4)     
        time.sleep(random.randint(2, 3))    

def getInfo():
    try:
        sum = 0
        #работа со статистикой
        with open("threadsdata/data.json", "r") as file:
            data = json.load(file)
            #время последнего обновления
            currenttime = data['lastupd']

            #парсинг полей money
            for post in data["thread"]:
                temp = post["money"]
                if temp.find('x') != -1:
                    sum = sum + int(post['money'].split("x")[0])*int(post['money'].split("x")[1])
                else:
                    sum+=int(post["money"])       
            file.close()
        return (f"Всего розыгрышей на сумму {sum}₽\nПоследнее обновление {currenttime}")
    except:
        return ("В базе нет записей")

if __name__ == '__main__':
    #name = ParserLolzChrome(False)
    #name.getAllPages()
    print(getInfo())
    