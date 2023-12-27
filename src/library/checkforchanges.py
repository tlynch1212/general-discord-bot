from bs4 import BeautifulSoup
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from markdownify import MarkdownConverter
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

        lastUpdateUrl = await getLastMessage(channel)

        if lastUpdateUrl != recentArticleUrl:
            embed = createEmbedPost(recentArticleUrl)
            await channel.send(embed=embed)
         
    except Exception as ex:
        print(ex)

async def getLastMessage(channel):
    lastUpdateUrl = ''
    try:
        lastUpdate = await channel.fetch_message(channel.last_message_id)
        return lastUpdate.embeds[0].url
    except Exception:
        return lastUpdateUrl

def createEmbedPost(articleUrl):
    articleHtml = fetchData(articleUrl)
    header = articleHtml.find('h1', {"class": "article-title"}).attrs['title']
    test = articleHtml.find("div", {"class": "article-body"})
    description = shortenDescription(MarkdownConverter().convert_soup(test).replace('\n\n', ''))
    embed = discord.Embed(url=articleUrl, title=header, description=description)
    embed.set_thumbnail(url=globalvariables.MINECRAFT_BLOCK_IMAGE)

    return embed

def shortenDescription(description):
    if len(description) <= 1000:
        return description
    
    descriptionStart = description[:1000]
    descriptionEnd = description[1000:]

    if descriptionStart.endswith('\n'):
        return descriptionStart
    else:
        return descriptionStart + descriptionEnd.split('\n', 1)[0] + '\n\n ...'


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

    service = webdriver.ChromeService(executable_path=binary_path)
    browser = webdriver.Chrome(options=options, service=service)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
    browser.get(url)
    html = browser.page_source
    browser.close()
    return BeautifulSoup(html, 'html.parser')