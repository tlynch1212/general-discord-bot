from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import discord
import library.globalvariables as globalvariables

async def check_for_minecraft_changes(channel):
    try:
        changelogs = fetchData(f"https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs")
        lists = changelogs.find_all('ul')
        recentArticleUrl = ''
        for list in lists:
            if 'article-list' in list.attrs['class'][0]:
                articles = list.find_all('li')
                for article in articles:
                    if 'Bedrock' in article.text:
                        recentArticleUrl = article.find('a').attrs['href']
                        break
                break
        recentArticleUrl = 'https://feedback.minecraft.net' + recentArticleUrl
        
        await channel.send(recentArticleUrl)
         
    except Exception as ex:
        print(ex)

def fetchData(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--incognito")
    options.add_argument("--nogpu")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1280")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    ua = UserAgent()
    userAgent = ua.random

    browser = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
    browser.get(url)
    html = browser.page_source
    browser.close()
    return BeautifulSoup(html, 'html.parser')