import discord
from discord.ext import commands
from discord import app_commands

from paddleocr import PaddleOCR


import pygetwindow
import pyautogui
from PIL import Image
import numpy as np
import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

ocr = PaddleOCR(use_angle_cls=False, lang='en', use_gpu=True, det_model_dir="en_number_mobile_v2.0_rec_infer.tar")

window = pygetwindow.getWindowsWithTitle("BlueStacks App Player")[0]
left, top = window.topleft
right, bottom = window.bottomright
window_width = right - left
window_height = bottom - top

crop_left = int(0.066 * window_width)     # 50px / 751px ~ 6.6%
crop_top = int(0.45 * window_height)     # 220px / 464px ~ 47.4%
crop_right = int(0.08 * window_width)    # 100px / 751px ~ 13.3% (751 - 100 = 651)
crop_bottom = int(0.08 * window_height)  # 10px / 464px ~ 2.2% (464 - 10 = 454)
crop_text = int(0.1731*window_width)

# 1. Create prompt
system_template = "This is my data {data}:"
prmt_template="""
i want you to correct the spelling boss name and calculate the percent base on the number given, just return like the format below, not any more word from you, not "Here is the corrected and formatted data:"

Lv.105 Viper Clan Leader (400,000,000/400,000,000) 100%
Lv.105 Lava Slime King (55,413,567/400,000,000) 12% 
Lv.105 Altered Mad Panda MK-3 (250,902,339/400,000,000) 55% 
Lv.105 Furious Desert BullWorm (93,698,474/ 400,000,000) 52%

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
    # Thực hiện sự kiện nhấp chuột
    # pyautogui.click(click_x, click_y)
    # # Đợi một chút để cửa sổ phản ứng
    # time.sleep(1) 
    window = pyautogui.screenshot(region=(left, top, window_width, window_height))
    window = window.crop((crop_left, crop_top, window_width - crop_right, window_height - crop_bottom))
    window = np.array(window)
    height, width, _ = window.shape
    window[height-crop_text:height, width-crop_text:width] = [255, 255, 255]
    result = ocr.ocr(window, cls=False)
    text_output = ""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text_output += line[1][0] + "\n"
            print(line)
    final = chain.invoke(text_output)
    # final = text_output
    await interaction.response.send_message(final)



client.run("")



        