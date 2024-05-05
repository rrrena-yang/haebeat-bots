import os
import discord
import datetime
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from discord.ext import commands
import requests

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def scrape(crew_name, dance_name):
    driver1 = webdriver.Chrome()
    driver1.get(f"https://www.coverdance.org/search?searcharea=contest&searchtype=2&searchtext={crew_name}")
    driver1.switch_to.frame(driver1.find_element(By.TAG_NAME, "iframe"))

    soup = BeautifulSoup(driver1.page_source, "html.parser")

    p = soup.find("p", string=re.compile(r'%s'%dance_name))
    dance = p.string.strip()
    nextSiblings = p.find_next_siblings() 
    media_info = nextSiblings[1].findChildren()
    views = media_info[1].string
    likes = media_info[2].string    
    return views, likes, dance


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.listen('on_message')
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$meow'):
        await message.channel.send('meow')
    elif message.content.startswith('$good boy'):
        await message.channel.send('(=^･ω･^=)')


@bot.listen('on_message')
async def on_message(message):
    if message.content.startswith('$bot_what'):
        await message.channel.send(
            '''Haebeat Magnetic
Haebeat Paint the Town
KORIGINS LALALA
VIVO BATTER UP
R.P.M Eve, Psyche & The Bluebeard\'s wife
Vivency Chasing That Feeling
Vivency Inception
KWNS HWAA
New Dawn Fever DICE
HAVOC Rock With You
''')

@bot.listen('on_message')
async def on_message(message):
    if message.content.startswith('$bot_check:'):
        msg_list = message.content.split()
        crew_name = msg_list[1]
        dance_name = msg_list[2]
        length = len(msg_list)
        i = 3
        while i < length:
            dance_name = dance_name + ' ' + msg_list[i]
            i = i + 1
        views, likes, dance = scrape(crew_name, dance_name)
        now = datetime.datetime.now()
        await message.channel.send(f"Crew: {crew_name}, Dance: {dance} \n{views} views, {likes} likes. \nRetrieved at: {now}")


@bot.listen('on_message')
async def on_message(message):
    if message.content.startswith('$bot_leaderboard'):
        response_param = message.content.split()[1]
        param = 0
        if response_param == 'view':
            param = 1
        else :
            param = 2
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"}
        r = requests.get(url=f'https://www.coverdance.org/contest/round1?type=R?page=2&year=14&area=NA&nationality=CA&sort={param}', headers=headers) 

        soup = BeautifulSoup(r.content, "html.parser")
        songs = soup.find_all("p", class_="song_info")
        i = 1
        await message.channel.send(f"Leaderboard with {response_param}")
        for song in songs:
            nextSiblings = song.find_next_siblings() 
            media_info = nextSiblings[1].findChildren()
            views = media_info[1].string
            likes = media_info[2].string 
            await message.channel.send(f"========={i}=========")
            await message.channel.send(f"Song: {song.string.strip()}")
            await message.channel.send(f"Team{song.find_next_siblings()[0].findChildren()[0].findChildren()[0].next_sibling.string.strip()}")
            await message.channel.send(f"Views: {views}")
            await message.channel.send(f"Likes: {likes}")
            i = i + 1


bot.run(DISCORD_TOKEN)