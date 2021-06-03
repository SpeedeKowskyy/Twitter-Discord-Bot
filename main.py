import tweepy, discord, json, asyncio, os, sys
from discord.ext import commands

#Functions
def check_files():
    if os.path.isfile("tweets.json"):
        pass
    else:
        f = open("tweets.json","w+")
        f.write("{\"a\": []}")
        f.close()
        print("tweets.json created")
    if os.path.isfile("pings.json"):
        pass
    else:
        f = open("pings.json","w+")
        f.write("{\"a\": []}")
        f.close()
        print("pings.json created")
    if os.path.isfile("tokens.py"):
        pass
    else:
        f = open("tokens.py", "w+")
        f.write("""
#Paste all of your tokens here

DISCORD_TOKEN = "" #Discord bot token"

#Twitter bot tokens
Access_Token = ""
Access_Token_Secret = ""

API_Key = ""
API_Secret_Key = ""

user = "" #User to pull tweets from
owner_id = "" #Your discord ID
bot_prefix = ".tweet " # !!! It is important that the prefix has a space at the end """)
        f.close()
        print("tokens.py created")

def write(dict_, filename):
    f = open("%s.json" % filename, "w")
    json.dump(dict(dict_), f)
    f.close()

def find(name, list_):
    for i in list_:
        if i == name:
            return True

def add_strings(list_):
    temp = " ".join(list_)
    return temp

check_files()
from tokens import *

if user == "":
    print("Make sure to fill all the variables in tokens.py")
    sys.exit()

client = commands.Bot(command_prefix=bot_prefix)

auth = tweepy.OAuthHandler(API_Key, API_Secret_Key)
auth.set_access_token(Access_Token, Access_Token_Secret)

api = tweepy.API(auth)

timeline = api.user_timeline(user)
site = "https://twitter.com/%s/status/" % user
id = ""
user_id = ""
temp_site = ""

@client.event
async def on_ready():
    print("Running")

@client.command()
async def start(ctx):
    while True:
        file2 = open("tweets.json", "r")
        fajl2 = json.load(file2)
        file2.close()
        timeline = api.user_timeline(user)
        id = timeline[0].id
        id = str(id)
        print("Checking: ", id)
        await asyncio.sleep(15)
        if find(id, fajl2["a"]):
            print("No new tweets.")
        else:
            fajl2["a"].append(id)
            write(fajl2, "tweets")
            print("New tweet found!")
            temp_site = site + str(id)
            file = open("pings.json", "r")
            fajl = json.load(file)
            file.close()
            await ctx.send("New tweet : %s \n%s" % (add_strings(fajl["a"]), temp_site))

@client.command()
async def add(ctx):
    user_id = str(ctx.message.author.id)
    user_id = ("<@%s>" % user_id)
    file = open("pings.json", "r")
    fajl = json.load(file)
    file.close()
    if find(user_id, fajl["a"]):
        await ctx.send("You're already on the list")
    else:
        fajl["a"].append(user_id)
        await ctx.send("Added to list")
    write(fajl, "pings")

@client.command()
async def remove(ctx):
    user_id = str(ctx.message.author.id)
    user_id = ("<@%s>" % user_id)
    file = open("pings.json", "r")
    fajl = json.load(file)
    file.close()
    if find(user_id, fajl["a"]):
        fajl["a"].remove(user_id)
        await ctx.send("Removed from list")
    else:
        await ctx.send("You're not on the list")
    write(fajl, "pings")

@client.command()
async def stop(ctx):
    if str(ctx.message.author.id) == owner_id:
        await ctx.send("Shutting down...")
        await ctx.bot.close()
    else:
        await ctx.send("You dont have the permission to do that.")

client.run(DISCORD_TOKEN)
