from selenium import webdriver # webdriver for checking update
from selenium.webdriver.common.by import By # shit i need to import "By"
from datetime import date # to specify today's date
import os # os interops
import time # time
import discord # yippieee
from discord import Webhook, SyncWebhook  # discord.py shit
import config # THE config file
import aiohttp # oops almost forgot this
import asyncio # kys
import win32gui

def checkVersion():
    # get current date
    today = date.today()
    yn = ""
    # browser shit!
    time.sleep(3)
    currDir = os.getcwd()
    webDrvPath = os.path.join(currDir, 'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--log-level=3')
    browser = webdriver.Chrome(executable_path=webDrvPath, chrome_options=options)
    # hide chromedriver console on Windows
    def enumWindowFunc(hwnd, windowList):
        """ win32gui.EnumWindows() callback """
        text = win32gui.GetWindowText(hwnd)
        className = win32gui.GetClassName(hwnd)
        if 'chromedriver' in text.lower() or 'chromedriver' in className.lower():
            win32gui.ShowWindow(hwnd, False)
    win32gui.EnumWindows(enumWindowFunc, [])
    # begin browser navigation
    # navigate to Kiddion's profile, as it has the latest thread link for his menu.
    browser.get("https://www.unknowncheats.me/forum/members/1861563.html")
    # click to the menu thread
    threadLink = browser.find_element(By.XPATH, '/html/body/div/table/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td/div/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div/ul/li[2]/dl/dd/div[3]/a[1]')
    threadLink = threadLink.get_attribute("href") # get thread link, reassign var then navigate to it
    browser.get(threadLink)
    # gather all links, filter for our targer url
    collectedElements = browser.find_elements(By.XPATH, '//*[@id="post_message_3525602"]/a')
    detectedElements = 0
    for a in collectedElements:
        if a.get_attribute('href') == config.currentVersionLink:
            detectedElements += 1
    if detectedElements >= 1:
        yn = "No."
    else:
        yn = "Yes! Go update."
    async def send_webhook():
        async with aiohttp.ClientSession() as session:
            # put your own webhook link here
            webhook = SyncWebhook.from_url('WEBHOOK-LINK-HERE')

            embed=discord.Embed(color=0x830b15)
            embed.set_thumbnail(url="https://www.unknowncheats.me/forum/customavatars/avatar1861563_4.gif")
            embed.add_field(name="Has Kiddion updated yet?", value=yn, inline=False)
            embed.add_field(name="Current Date", value=today, inline=True)
            embed.set_footer(text="Kiddion's Modest Menu Update Checker")
            if detectedElements >= 1:
                await webhook.send(embed=embed)
            else:
                # replace INSERT-ID with your own Discord User ID
                await webhook.send(content="<@INSERT-ID>", embed=embed)
    try:
        asyncio.run(send_webhook())
    except:
        pass

checkVersion()

