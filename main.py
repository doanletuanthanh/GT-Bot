import discord
from discord.ext import commands
from discord import app_commands

from paddleocr import PaddleOCR


import pygetwindow
import pyautogui
from PIL import Image
import numpy as np

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

ocr = PaddleOCR(use_angle_cls=False, lang='en', use_gpu=True, det_model_dir="en_number_mobile_v2.0_rec_infer.tar")
# img_path = 'test-image-2.jpg'

window = pygetwindow.getWindowsWithTitle("BlueStacks App Player")[0]
left, top = window.topleft
right, bottom = window.bottomright


system_template = "This is my data {data}:"
prmt_template="""
i want you to correct the spelling and calculate the percent hp boss, just return like the format below, not any more word from you, not "Here is the corrected and formatted data:"

Lv.105 Founder Elphaba (305,330,795/400,000,000) 75% 
Lv.105 Goblin Chief (55,413,567/400,000,000) 12% 
Lv.105 Nine-tailed Fox Garam (93,698,474/400,000,000) 25% 
Lv.105 Snowman General Gast (250,902,339/ 400,000,000) 55%

"""
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', prmt_template)
])

# 2. Create model
model = ChatGroq(model="llama3-8b-8192", api_key='')

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

        try: 
            guild = discord.Object(id=1134890205460041858)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} command(s) to guild {guild.id}.')
        except Exception as e:
            print(f"Error syncing commands: {e}")


    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('dit me'):
            await message.channel.send(f'Dit me {message.author}!')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('React cc')
    

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)

GUILD_ID = discord.Object(id=1134890205460041858)


@client.tree.command(name="hello", description="Says hello", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message('Hello!')

@client.tree.command(name="bosscheck", description="Kiem tra dmg boss", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):

    a = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    a = a.crop((50, 220, right - left - 100, bottom - top - 10))
    a = np.array(a)
    height, width, _ = a.shape
    a[height-130:height, width-130:width] = [255, 255, 255]
    result = ocr.ocr(a, cls=False)
    text_output = ""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text_output += line[1][0] + "\n"
    final = chain.invoke(text_output)
    await interaction.response.send_message(final)



client.run("")



        