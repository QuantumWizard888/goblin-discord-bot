
#? discord_bot.py - Discord bot
#? v0.4

import discord
from discord.ext import commands, tasks
from discord import Status, File
import random
import datetime
import os
import urllib.parse
import requests
import json
from lxml import html
from bs4 import BeautifulSoup

VER = '0.4'

# <--- Config
config = {
    'token': '', # Put your token here
    'prefix': 'g>',
}
# --->


# <--- Bot init
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
# --->


# <--- Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    
    if ctx.author != bot.user and isinstance(error, commands.CommandNotFound):

        author = ctx.message.author
        message_content = ctx.message.content

        await ctx.reply(f'{author.mention} I have no idea what you wrote here "{message_content}"')
# --->


# <--- version_command
@bot.command(name='version')
async def version_command(ctx):

    if ctx.author != bot.user:
                
        author = ctx.message.author
       
        await ctx.reply(f'{author.mention} My version: {VER}')
# --->


# <--- helpme_command
with open('helpme_command_answers.txt', 'r', encoding= 'utf-8') as helpme_answers_file:
    helpme_answers_list = [i.rstrip('\n') for i in helpme_answers_file.readlines()]
    helpme_answers = '\n'.join(helpme_answers_list)

@bot.command(name='helpme')
async def helpme_command(ctx):

    if ctx.author != bot.user:
                
        author = ctx.message.author
       
        await ctx.reply(f'{author.mention} My name is Goblin from Underworld. Do not disturb my silence, kid. Here what I can:\n'+helpme_answers)
# --->


# <--- attack_command
attack_command_aliases = ['Give_slap', 'give_slap', 'Hit', 'hit', 'Kick', 'kick']
attack_img_files = [f for f in os.listdir(os.curdir+'/attack_imgs/')]


with open('attack_command_answers.txt', 'r', encoding= 'utf-8') as attack_answers_file:
    attack_answers = [i.rstrip('\n') for i in attack_answers_file.readlines()]


@bot.command(name='attack', aliases = attack_command_aliases)
async def attack_command(ctx):
    
    if ctx.author != bot.user:

        if not bot.user.mentioned_in(ctx.message):

            attack_answer = random.choice(attack_answers)
            attack_img_answer = File(os.curdir+'/attack_imgs/'+random.choice(attack_img_files), filename='attack_img.png')
            # embed = discord.Embed()
            # embed.set_image(url="attachment://attack_img")

            await ctx.reply(f'{attack_answer} <@{ctx.message.mentions[0].id}>', file = attack_img_answer)
        
        elif bot.user.mentioned_in(ctx.message):
            
            #author = ctx.author.id
            author = ctx.message.author

            await ctx.reply(f'{author.mention} Don\'t you want to get punched in the face, smart guy?!')
# --->


# <--- hello_command
hello_command_aliases = ['Hello', 'hello', 'Hi', 'hi', 'Howdy', 'howdy', 'Greetings', 'greetings']


with open('hello_command_answers.txt', 'r', encoding= 'utf-8') as hello_answers_file:
    hello_answers = [i.rstrip('\n') for i in hello_answers_file.readlines()]


@bot.command(name='hello', aliases = hello_command_aliases)
async def hello_command(ctx):

    if ctx.author != bot.user:
                
        author = ctx.message.author
        hello_answer = random.choice(hello_answers)
    
        await ctx.reply(f'{author.mention} {hello_answer}')
# --->


# <--- calc_command
@bot.command(name='calc')
async def calc_command(ctx, arg):

    expression = arg
    expression_url_enc = urllib.parse.quote(expression)

    page = requests.get('http://api.mathjs.org/v4/?expr='+expression_url_enc)
    
    await ctx.reply(f'{page.content.decode("utf-8")}')
# --->


# <--- money_forex_command
@bot.command(name='money_forex')
async def money_forex_command(ctx):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
        }

    cur_forex_dict = {
        "usd": "US Dollar", 
        'eur': "Euro", 
        "gbp": "British Pound", 
        "chf": "Swiss Franc", 
        "cny": "Chinese Yuan", 
        "jpy": "Japanese Yen"
        }

    money_report = 'Currencies quotes on FOREX for our immortal rubble'+'\n'

    for c_f_k in cur_forex_dict:

        money_page_forex_url = 'https://ru.investing.com/currencies/'+c_f_k+'-rub'
        money_page_forex = requests.get(money_page_forex_url, headers=headers)

        html = money_page_forex.text
        soup = BeautifulSoup(html, 'lxml')

        currency_val = soup.find('div', attrs= {'data-test': 'instrument-price-last'}).text
        
        money_report_c_f = ''

        c_f_title = '--- '+c_f_k.upper()+' - '+cur_forex_dict[c_f_k]+' ---\n'
        c_f_val = 'Current:\t\t\t  '+ currency_val + '\n'

        money_report_c_f +=c_f_title + c_f_val
        money_report += money_report_c_f
        money_report_c_f = ''
    
    await ctx.reply(money_report)
# --->


# <--- money_command
@bot.command(name='money')
async def money_command(ctx):

    money_page = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    money_page_json = money_page.content.decode("utf-8")
    money_page = json.loads(money_page_json)

    cur_dict = {
        "USD": "US Dollar", 
        'EUR': "Euro", 
        "GBP": "British Pound", 
        "CHF": "Swiss Franc", 
        "CNY": "Chinese Yuan", 
        "JPY": "Japanese Yen"
        }

    money_report = 'Currencies quotes set by RU Central bank for today: '+datetime.datetime.now().strftime("%d.%m.%Y")+'\n'
    
    for c_k in cur_dict:

        money_report_c = ''

        c_title = '--- '+c_k+' - '+cur_dict[c_k]+' ---\n'
        c_val_cur = 'Current:\t\t\t  '+str(money_page['Valute'][c_k]['Value']) + '\n'
        c_val_prev = 'Previous:\t'+str(money_page['Valute'][c_k]['Previous']) + '\n'
        c_val_delta = 'Delta:\t\t\t\t\t ' + str(round(money_page['Valute'][c_k]['Value'] - money_page['Valute'][c_k]['Previous'], 4)) + '\n'

        money_report_c +=c_title + c_val_cur + c_val_prev + c_val_delta
        money_report += money_report_c
        money_report_c = ''
    
    await ctx.reply(money_report)
# --->


# <--- tamriel_day_command
@bot.command(name='tamriel_day')
async def tamriel_day_command(ctx):
    
    week_day = {
        1: 'Morndas',
        2: 'Tirdas',
        3: 'Middas',
        4: 'Turdas',
        5: 'Fredas',
        6: 'Loredas',
        7: 'Sundas'
    }

    month = {
        1: 'Morning Star',
        2: 'Sun’s Dawn',
        3: 'First Seed',
        4: 'Rain’s Hand',
        5: 'Second Seed',
        6: 'Mid Year',
        7: 'Sun’s Height',
        8: 'Last Seed',
        9: 'Hearthfire',
        10: 'Frostfall',
        11: 'Sun’s Dusk',
        12: 'Evening Star'
    }   

    await ctx.reply(f'Today is {week_day[datetime.datetime.today().weekday()+1]}, {datetime.datetime.today().day} of {month[datetime.datetime.today().month]}')
# --->


# <--- Stream notification task
local_tz = datetime.datetime.now().astimezone().tzinfo
time_schedule = [
    datetime.time(hour=15, minute=00,  second = 00, tzinfo=local_tz),
    datetime.time(hour=15, minute=10,  second = 00, tzinfo=local_tz),
    datetime.time(hour=15, minute=20,  second = 00, tzinfo=local_tz),
    datetime.time(hour=15, minute=30,  second = 00, tzinfo=local_tz),
    datetime.time(hour=15, minute=40,  second = 00, tzinfo=local_tz),
    datetime.time(hour=15, minute=50,  second = 00, tzinfo=local_tz)
]


@tasks.loop(time = time_schedule)
async def stream_notification_task():
    
    guild_m = bot.get_guild() # Put Guild ID here
    channel_m = bot.get_channel() # Put Channel ID here
    user_m = await bot.fetch_user() # Put User ID here (User ID == Member ID)
    member_m = guild_m.get_member() # Put Member ID here (Member ID == User ID)
    
    # for member_i in guild_m.members:
    #     print(member_i.name, member_i.id, member_i.status)

    if datetime.datetime.today().weekday() == 4 and member_m.status == Status.offline:
        
        await channel_m.send(f'<@{user_m.id}>, WHERE ARE YOU???? HMMMMMMM????')


@bot.event
async def on_ready():

    stream_notification_task.start()
# --->

        
# <--- Run bot
bot.run(config['token'])
# --->
