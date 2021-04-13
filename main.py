import discord
import asyncio
import schedule
import time
from discord.ext import tasks
import speech_recognition as sr
from requests import get
from pygame import mixer
app = discord.Client()

#channel_id = "your_channel_id"
channel_id = "754711446402891776"
server_bot_id = "example#0000"
client_bot_id = "example2#0000" #Edit to your Server and Client bot id

can_use_start = False
a = 0
def get_token(): # Get tokens from key.key
    with open("Key.key", "r") as f:
        return f.readline().strip()

def stt_func():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening")
        audio = r.listen(source)
    return r.recognize_google(audio, language='ko')

def tts_func(sentence):
    global a
    file_name = "now_" + str(a) + ".mp3"
    a = a+1
    with open(file_name, "wb") as file:
        url = str("https://tts-translate.kakao.com/newtone?message=") + str(sentence) + str("&format=wav-16k")
        response = get(url)
        file.write(response.content)
        file.close()

    mixer.init()
    mixer.music.load(file_name)
    mixer.music.play()

@tasks.loop(seconds = 5.0)
async def start_input():
    global can_use_start
    if can_use_start == False:
        return None
    tmp = str(input("Start를 입력하셔서 인공지능을 사용하세요!\n"))
    if tmp == "Start":
        can_use_start = False
        channel = app.get_channel(str(channel_id))
        await channel.send("??test")

@app.event
async def on_ready():
    global can_use_start
    print("Logining to : " + str(app.user.name) + "(code : " + str(app.user.id) + ")")
    game = discord.Game("Running program.....")
    await app.change_presence(status=discord.Status.online, activity=game)
    print("Bot is started!")
    can_use_start = True

@app.event
async def on_message(message):
    global can_use_start
    if str(message.author) == str(client_bot_id):
        if message.content == "??test":
            pass
        else:
            return None
    elif str(message.author) == str(server_bot_id):
        pass
    else:
        return None
    if message.content == "??test":
        await message.channel.send("코이야 " + stt_func())
    if message.content[:5] == "호출어0 ":
        tts_func(message.content[6:])
        can_use_start = True

start_input.start()
app.run(get_token())
print("a")
